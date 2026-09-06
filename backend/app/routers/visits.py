import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import SiteVisit, Enquiry, User, Property
from app.schemas import VisitBookRequest, VisitBookResponse, VisitOut, VisitFeedback, PostponeRequest
from app.routers.auth import get_current_user, require_admin
from app.services.notification_service import notify, log_activity
from app.config import get_settings

router = APIRouter(prefix="/visits", tags=["Visits"])

def _parse_dt(date_str: str, time_str: str) -> datetime:
    for fmt in ("%I:%M %p", "%I:%M%p", "%H:%M", "%I %p"):
        try:
            t = datetime.strptime(time_str.strip().upper(), fmt)
            return datetime.fromisoformat(f"{date_str}T{t.strftime('%H:%M:%S')}")
        except ValueError: continue
    return datetime.fromisoformat(f"{date_str}T10:00:00")

def check_conflicts(db: Session, scheduled: datetime, slot_mins: int, exclude_id: str = None):
    """Check for overlapping appointments within the time slot."""
    start = scheduled
    end = scheduled + timedelta(minutes=slot_mins)
    q = db.query(SiteVisit).filter(
        SiteVisit.status.in_(["scheduled", "confirmed"]),
        SiteVisit.scheduled_date < end,
    )
    if exclude_id: q = q.filter(SiteVisit.id != exclude_id)
    conflicts = []
    for v in q.all():
        v_end = v.end_time or (v.scheduled_date + timedelta(minutes=slot_mins))
        if v.scheduled_date < end and v_end > start:
            conflicts.append(v)
    return conflicts

def auto_assign(db: Session) -> Optional[User]:
    agents = db.query(User).filter(User.role.in_(["sales_agent", "sales_manager"]), User.is_active == True).all()
    if not agents: return None
    counts = {a.id: db.query(SiteVisit).filter(SiteVisit.assigned_agent == a.id, SiteVisit.status.in_(["scheduled", "confirmed"])).count() for a in agents}
    best = min(counts, key=counts.get)
    return next(a for a in agents if a.id == best)

@router.post("/book", response_model=VisitBookResponse)
def book(body: VisitBookRequest, db: Session = Depends(get_db)):
    scheduled = _parse_dt(body.preferred_date, body.preferred_time)
    slot = get_settings().visit_slot_minutes
    end_time = scheduled + timedelta(minutes=slot)

    # Check conflicts
    conflicts = check_conflicts(db, scheduled, slot)
    if conflicts:
        # Find next available slot
        latest_end = max(c.end_time or (c.scheduled_date + timedelta(minutes=slot)) for c in conflicts)
        suggested = latest_end + timedelta(minutes=15)
        return VisitBookResponse(
            visit_id="", status="conflict", scheduled_date=suggested, conflict=True,
            message=f"That time slot is taken. Next available: {suggested.strftime('%B %d at %I:%M %p')}. Would you like to book that instead?"
        )

    agent = auto_assign(db)
    prop_name = body.property_name
    if body.property_id:
        prop = db.query(Property).filter(Property.id == body.property_id).first()
        if prop: prop_name = prop.name

    visit = SiteVisit(
        id=str(uuid.uuid4()), enquiry_id=body.enquiry_id, buyer_name=body.buyer_name,
        buyer_phone=body.buyer_phone, buyer_email=body.buyer_email or "",
        property_id=body.property_id, property_name=prop_name or "TBD",
        scheduled_date=scheduled, end_time=end_time, status="scheduled",
        assigned_agent=agent.id if agent else None, agent_name=agent.full_name if agent else "", notes=body.notes or "")
    db.add(visit)

    if body.enquiry_id:
        enq = db.query(Enquiry).filter(Enquiry.id == body.enquiry_id).first()
        if enq: enq.status = "visit_booked"

    # Notify admins
    for admin in db.query(User).filter(User.role.in_(["admin", "sales_manager"])).all():
        notify(db, f"New tour: {body.buyer_name}", f"{prop_name} on {body.preferred_date} at {body.preferred_time}", "visit", admin.id)
    log_activity(db, "Tour booked", entity_type="visit", entity_id=visit.id, details=f"{body.buyer_name} — {prop_name}")
    db.commit()

    return VisitBookResponse(visit_id=visit.id, status="scheduled", scheduled_date=scheduled,
                             message=f"Tour booked for {body.preferred_date} at {body.preferred_time}! {agent.full_name if agent else 'An agent'} will meet you there.")

@router.get("/list", response_model=List[VisitOut])
def list_visits(status: Optional[str] = None, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    q = db.query(SiteVisit).order_by(SiteVisit.scheduled_date.desc())
    if u.role == "customer":
        q = q.filter((SiteVisit.customer_id == u.id) | (SiteVisit.buyer_email == u.email))
    if status: q = q.filter(SiteVisit.status == status)
    return [VisitOut.model_validate(v) for v in q.limit(100).all()]

@router.get("/my-visits", response_model=List[VisitOut])
def my_visits(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    visits = db.query(SiteVisit).filter(
        (SiteVisit.customer_id == u.id) | (SiteVisit.buyer_email == u.email)
    ).order_by(SiteVisit.scheduled_date.desc()).all()
    return [VisitOut.model_validate(v) for v in visits]

@router.patch("/{vid}/status")
def update_status(vid: str, new_status: str = Query(...), db: Session = Depends(get_db), u: User = Depends(require_admin)):
    v = db.query(SiteVisit).filter(SiteVisit.id == vid).first()
    if not v: raise HTTPException(404)
    v.status = new_status; v.updated_at = datetime.utcnow()
    log_activity(db, f"Visit {new_status}", actor="staff", entity_type="visit", entity_id=vid)
    db.commit()
    return {"id": vid, "status": new_status}

@router.post("/{vid}/postpone")
def postpone(vid: str, body: PostponeRequest, db: Session = Depends(get_db), u: User = Depends(require_admin)):
    v = db.query(SiteVisit).filter(SiteVisit.id == vid).first()
    if not v: raise HTTPException(404)
    new_dt = _parse_dt(body.new_date, body.new_time)
    slot = get_settings().visit_slot_minutes
    conflicts = check_conflicts(db, new_dt, slot, exclude_id=vid)
    if conflicts:
        raise HTTPException(409, f"New time conflicts with {len(conflicts)} existing appointment(s). Please pick another time.")
    old_date = v.scheduled_date.strftime("%B %d at %I:%M %p")
    v.scheduled_date = new_dt
    v.end_time = new_dt + timedelta(minutes=slot)
    v.status = "postponed"
    v.postpone_reason = body.reason
    v.updated_at = datetime.utcnow()
    # Notify the customer
    if v.customer_id:
        notify(db, "Your tour has been rescheduled",
               f"New time: {new_dt.strftime('%B %d at %I:%M %p')}. Reason: {body.reason}",
               "visit", v.customer_id)
    log_activity(db, f"Tour postponed from {old_date}", actor="staff", entity_type="visit", entity_id=vid, details=body.reason)
    db.commit()
    return {"id": vid, "status": "postponed", "new_date": new_dt.isoformat(), "message": "Tour rescheduled and customer notified."}

@router.post("/{vid}/feedback")
def submit_feedback(vid: str, body: VisitFeedback, db: Session = Depends(get_db)):
    v = db.query(SiteVisit).filter(SiteVisit.id == vid).first()
    if not v: raise HTTPException(404)
    v.feedback = body.feedback; v.rating = body.rating; v.status = "completed"; db.commit()
    return {"ok": True}
