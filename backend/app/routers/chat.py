import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Enquiry, ChatMessage, User
from app.schemas import ChatRequest, ChatResponse, ChatHistoryOut
from app.services.ai_service import get_ai_service
from app.services.notification_service import notify, log_activity

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/message", response_model=ChatResponse)
async def send_message(body: ChatRequest, db: Session = Depends(get_db)):
    enquiry = db.query(Enquiry).filter(Enquiry.id == body.enquiry_id).first() if body.enquiry_id else None
    if not enquiry:
        enquiry = Enquiry(id=str(uuid.uuid4()), buyer_name=body.buyer_name or "Visitor",
                          buyer_phone=body.buyer_phone or "", buyer_email=body.buyer_email or "",
                          source="website", status="new")
        db.add(enquiry); db.flush()
        # Notify all admins
        for admin in db.query(User).filter(User.role.in_(["admin", "sales_manager"])).all():
            notify(db, f"New enquiry from {enquiry.buyer_name}", "Via AI chat", "enquiry", admin.id)
        log_activity(db, "New enquiry from AI chat", entity_type="enquiry", entity_id=enquiry.id, details=enquiry.buyer_name)

    db.add(ChatMessage(id=str(uuid.uuid4()), enquiry_id=enquiry.id, sender="buyer", content=body.message))
    result = await get_ai_service().generate_response(body.message)
    db.add(ChatMessage(id=str(uuid.uuid4()), enquiry_id=enquiry.id, sender="agent", content=result["reply"],
                       message_type="escalation" if result.get("escalated") else "text", intent=result.get("intent", "")))
    enquiry.message_count = (enquiry.message_count or 0) + 2
    enquiry.last_agent_message = result["reply"][:200]
    if result.get("escalated"):
        enquiry.status = "escalated"; enquiry.priority = "urgent"
        for admin in db.query(User).filter(User.role.in_(["admin", "sales_manager"])).all():
            notify(db, f"⚠ Escalation: {enquiry.buyer_name}", f"Intent: {result['intent']}", "escalation", admin.id)
    elif enquiry.status == "new": enquiry.status = "contacted"
    db.commit()
    return ChatResponse(enquiry_id=enquiry.id, reply=result["reply"], intent=result.get("intent", ""),
                        suggested_actions=result.get("suggested_actions", []), escalated=result.get("escalated", False))

@router.get("/history/{enquiry_id}", response_model=List[ChatHistoryOut])
def get_history(enquiry_id: str, db: Session = Depends(get_db)):
    return [ChatHistoryOut.model_validate(m) for m in db.query(ChatMessage).filter(ChatMessage.enquiry_id == enquiry_id).order_by(ChatMessage.created_at).all()]
