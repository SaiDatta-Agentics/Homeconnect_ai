import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.database import get_db
from app.models import Enquiry, SiteVisit, Property, User
from app.schemas import EnquiryCreate, EnquiryOut, EnquiryUpdate
from app.routers.auth import get_current_user, require_admin

router = APIRouter(prefix="/enquiries", tags=["Enquiries"])

@router.post("/create", response_model=EnquiryOut)
def create_enquiry(body: EnquiryCreate, db: Session = Depends(get_db), u: User = Depends(require_admin)):
    enq = Enquiry(id=str(uuid.uuid4()), **body.model_dump(), assigned_to=u.id)
    db.add(enq); db.commit(); db.refresh(enq)
    return EnquiryOut.model_validate(enq)

@router.get("/list", response_model=List[EnquiryOut])
def list_enquiries(status: Optional[str] = None, db: Session = Depends(get_db), u: User = Depends(require_admin)):
    q = db.query(Enquiry).order_by(Enquiry.created_at.desc())
    if status: q = q.filter(Enquiry.status == status)
    return [EnquiryOut.model_validate(e) for e in q.limit(200).all()]

@router.patch("/{eid}", response_model=EnquiryOut)
def update_enquiry(eid: str, body: EnquiryUpdate, db: Session = Depends(get_db), u: User = Depends(require_admin)):
    e = db.query(Enquiry).filter(Enquiry.id == eid).first()
    if not e: raise HTTPException(404)
    for f, v in body.model_dump(exclude_unset=True).items(): setattr(e, f, v)
    db.commit(); db.refresh(e)
    return EnquiryOut.model_validate(e)

@router.get("/stats/summary")
def stats(db: Session = Depends(get_db), u: User = Depends(require_admin)):
    total_enq = db.query(Enquiry).count()
    total_vis = db.query(SiteVisit).count()
    total_prop = db.query(Property).count()
    by_status = {s: db.query(Enquiry).filter(Enquiry.status == s).count() for s in ["new","contacted","qualified","visit_booked","escalated","converted","lost"]}
    vis_by_status = {s: db.query(SiteVisit).filter(SiteVisit.status == s).count() for s in ["scheduled","confirmed","completed","cancelled","postponed"]}
    by_source = dict(db.query(Enquiry.source, func.count()).group_by(Enquiry.source).all())
    converted = by_status.get("converted", 0)
    conv_rate = round(converted / total_enq * 100, 1) if total_enq > 0 else 0
    from datetime import datetime, timedelta
    daily_enq = [{"date": (datetime.utcnow() - timedelta(days=13-i)).date().isoformat(),
                   "count": db.query(Enquiry).filter(func.date(Enquiry.created_at) == (datetime.utcnow() - timedelta(days=13-i)).date()).count()} for i in range(14)]
    top_props = [{"property": r[0], "count": r[1]} for r in db.query(Enquiry.property_interest, func.count()).group_by(Enquiry.property_interest).order_by(func.count().desc()).limit(5).all() if r[0]]
    agent_perf = [{"name": a.full_name, "assigned": db.query(Enquiry).filter(Enquiry.assigned_to == a.id).count(),
                   "visits_completed": db.query(SiteVisit).filter(SiteVisit.assigned_agent == a.id, SiteVisit.status == "completed").count()}
                  for a in db.query(User).filter(User.role.in_(["sales_agent", "sales_manager"])).all()]
    return {"total_enquiries": total_enq, "total_visits": total_vis, "total_properties": total_prop,
            "enquiries_by_status": by_status, "visits_by_status": vis_by_status, "enquiries_by_source": by_source,
            "conversion_rate": conv_rate, "daily_enquiries": daily_enq, "top_properties": top_props, "agent_performance": agent_perf}
