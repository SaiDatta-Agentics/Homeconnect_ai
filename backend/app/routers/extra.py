import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Property, Notification, ActivityLog, User
from app.schemas import PropertyOut, PropertyCreate, NotificationOut
from app.routers.auth import get_current_user, require_admin
from app.services.notification_service import log_activity

# ── Properties (public list, admin CRUD) ──
properties_router = APIRouter(prefix="/properties", tags=["Properties"])

@properties_router.get("/list", response_model=List[PropertyOut])
def list_properties(db: Session = Depends(get_db)):
    return [PropertyOut.model_validate(p) for p in db.query(Property).order_by(Property.price_usd).all()]

@properties_router.get("/{pid}", response_model=PropertyOut)
def get_property(pid: str, db: Session = Depends(get_db)):
    p = db.query(Property).filter(Property.id == pid).first()
    if not p: raise HTTPException(404)
    return PropertyOut.model_validate(p)

@properties_router.post("/create", response_model=PropertyOut)
def create_property(body: PropertyCreate, db: Session = Depends(get_db), u: User = Depends(require_admin)):
    p = Property(id=str(uuid.uuid4()), **body.model_dump(), created_by=u.id)
    if p.total_area_sqft > 0 and p.price_usd > 0:
        p.price_per_sqft = round(p.price_usd / p.total_area_sqft, 2)
    db.add(p); db.commit(); db.refresh(p)
    log_activity(db, f"Property added: {p.name}", actor="staff", entity_type="property", entity_id=p.id)
    db.commit()
    return PropertyOut.model_validate(p)

@properties_router.patch("/{pid}", response_model=PropertyOut)
def update_property(pid: str, body: PropertyCreate, db: Session = Depends(get_db), u: User = Depends(require_admin)):
    p = db.query(Property).filter(Property.id == pid).first()
    if not p: raise HTTPException(404)
    for f, v in body.model_dump(exclude_unset=True).items(): setattr(p, f, v)
    if p.total_area_sqft > 0 and p.price_usd > 0:
        p.price_per_sqft = round(p.price_usd / p.total_area_sqft, 2)
    db.commit(); db.refresh(p)
    return PropertyOut.model_validate(p)

@properties_router.delete("/{pid}")
def delete_property(pid: str, db: Session = Depends(get_db), u: User = Depends(require_admin)):
    p = db.query(Property).filter(Property.id == pid).first()
    if not p: raise HTTPException(404)
    db.delete(p); db.commit()
    return {"ok": True}

# ── Notifications ──
notifications_router = APIRouter(prefix="/notifications", tags=["Notifications"])

@notifications_router.get("/list", response_model=List[NotificationOut])
def list_notifications(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return [NotificationOut.model_validate(n) for n in db.query(Notification).filter(
        (Notification.user_id == u.id) | (Notification.user_id == None)).order_by(Notification.created_at.desc()).limit(50).all()]

@notifications_router.post("/{nid}/read")
def mark_read(nid: str, db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    n = db.query(Notification).filter(Notification.id == nid).first()
    if n: n.is_read = True; db.commit()
    return {"ok": True}

@notifications_router.post("/read-all")
def mark_all_read(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    db.query(Notification).filter((Notification.user_id == u.id) | (Notification.user_id == None), Notification.is_read == False).update({Notification.is_read: True})
    db.commit()
    return {"ok": True}

@notifications_router.get("/unread-count")
def unread_count(db: Session = Depends(get_db), u: User = Depends(get_current_user)):
    return {"count": db.query(Notification).filter((Notification.user_id == u.id) | (Notification.user_id == None), Notification.is_read == False).count()}

# ── Activity ──
activity_router = APIRouter(prefix="/activity", tags=["Activity"])

@activity_router.get("/feed")
def activity_feed(db: Session = Depends(get_db), u: User = Depends(require_admin)):
    return [{"id": a.id, "actor": a.actor, "action": a.action, "entity_type": a.entity_type,
             "entity_id": a.entity_id, "details": a.details, "created_at": a.created_at}
            for a in db.query(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(50).all()]
