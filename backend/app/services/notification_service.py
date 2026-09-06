import uuid
from sqlalchemy.orm import Session
from app.models import Notification, ActivityLog

def notify(db: Session, title: str, body: str = "", category: str = "info", user_id: str = None, link: str = ""):
    db.add(Notification(id=str(uuid.uuid4()), user_id=user_id, title=title, body=body, category=category, link=link))
    db.flush()

def log_activity(db: Session, action: str, actor: str = "agent", entity_type: str = "", entity_id: str = "", details: str = ""):
    db.add(ActivityLog(id=str(uuid.uuid4()), actor=actor, action=action, entity_type=entity_type, entity_id=entity_id, details=details))
    db.flush()
