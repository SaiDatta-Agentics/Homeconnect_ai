import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

def uid(): return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=uid)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, default="")
    role = Column(String, default="customer")  # customer | admin | sales_manager | sales_agent
    is_active = Column(Boolean, default=True)
    avatar_color = Column(String, default="#2563eb")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Property(Base):
    __tablename__ = "properties"
    id = Column(String, primary_key=True, default=uid)
    name = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    property_type = Column(String, nullable=False)
    total_area_sqft = Column(Integer, default=0)
    price_usd = Column(Integer, default=0)
    price_per_sqft = Column(Float, default=0.0)
    bedrooms = Column(Integer, default=3)
    bathrooms = Column(Integer, default=2)
    floor_number = Column(Integer, nullable=True)
    total_floors = Column(Integer, default=0)
    facing = Column(String, default="")
    status = Column(String, default="available")  # available | reserved | sold
    parking = Column(Integer, default=1)
    amenities = Column(Text, default="")
    completion_date = Column(String, default="")
    description = Column(Text, default="")
    location = Column(String, default="")
    address = Column(String, default="")
    city = Column(String, default="")
    state = Column(String, default="")
    country = Column(String, default="USA")
    zip_code = Column(String, default="")
    image_url = Column(String, default="")
    mls_id = Column(String, default="")
    year_built = Column(Integer, default=2024)
    lot_size_sqft = Column(Integer, default=0)
    hoa_monthly = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, ForeignKey("users.id"), nullable=True)

class Enquiry(Base):
    __tablename__ = "enquiries"
    id = Column(String, primary_key=True, default=uid)
    customer_id = Column(String, ForeignKey("users.id"), nullable=True)
    buyer_name = Column(String, nullable=False)
    buyer_phone = Column(String, nullable=False)
    buyer_email = Column(String, default="")
    source = Column(String, default="website")
    status = Column(String, default="new")
    property_interest = Column(String, default="")
    budget_range = Column(String, default="")
    notes = Column(Text, default="")
    assigned_to = Column(String, ForeignKey("users.id"), nullable=True)
    priority = Column(String, default="medium")
    last_agent_message = Column(Text, default="")
    message_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages = relationship("ChatMessage", back_populates="enquiry", order_by="ChatMessage.created_at")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(String, primary_key=True, default=uid)
    enquiry_id = Column(String, ForeignKey("enquiries.id"), nullable=False, index=True)
    sender = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String, default="text")
    intent = Column(String, default="")
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    enquiry = relationship("Enquiry", back_populates="messages")

class SiteVisit(Base):
    __tablename__ = "site_visits"
    id = Column(String, primary_key=True, default=uid)
    enquiry_id = Column(String, ForeignKey("enquiries.id"), nullable=True)
    customer_id = Column(String, ForeignKey("users.id"), nullable=True)
    buyer_name = Column(String, nullable=False)
    buyer_phone = Column(String, nullable=False)
    buyer_email = Column(String, default="")
    property_id = Column(String, ForeignKey("properties.id"), nullable=True)
    property_name = Column(String, default="")
    scheduled_date = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default="scheduled")  # scheduled | confirmed | completed | cancelled | postponed
    assigned_agent = Column(String, ForeignKey("users.id"), nullable=True)
    agent_name = Column(String, default="")
    feedback = Column(Text, default="")
    rating = Column(Integer, nullable=True)
    notes = Column(Text, default="")
    postpone_reason = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True, default=uid)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    body = Column(Text, default="")
    category = Column(String, default="info")
    is_read = Column(Boolean, default=False)
    link = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_log"
    id = Column(String, primary_key=True, default=uid)
    actor = Column(String, default="agent")
    action = Column(String, nullable=False)
    entity_type = Column(String, default="")
    entity_id = Column(String, default="")
    details = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
