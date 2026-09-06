from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    email: str; password: str

class RegisterRequest(BaseModel):
    email: str; password: str; full_name: str; phone: str = ""
    role: str = "customer"

class UserOut(BaseModel):
    id: str; email: str; full_name: str; phone: str; role: str
    is_active: bool; avatar_color: str; created_at: datetime
    class Config: from_attributes = True

class LoginResponse(BaseModel):
    access_token: str; token_type: str = "bearer"; user: UserOut

class TokenData(BaseModel):
    sub: str; name: str; role: str

class ChatRequest(BaseModel):
    enquiry_id: Optional[str] = None; message: str
    buyer_name: Optional[str] = None; buyer_phone: Optional[str] = None
    buyer_email: Optional[str] = None

class ChatResponse(BaseModel):
    enquiry_id: str; reply: str; intent: str
    suggested_actions: List[str] = []; escalated: bool = False
    confidence: float = 1.0

class ChatHistoryOut(BaseModel):
    id: str; sender: str; content: str; message_type: str; intent: str; created_at: datetime
    class Config: from_attributes = True

class VisitBookRequest(BaseModel):
    enquiry_id: Optional[str] = None; buyer_name: str; buyer_phone: str
    buyer_email: Optional[str] = ""; property_name: Optional[str] = ""
    property_id: Optional[str] = None
    preferred_date: str; preferred_time: str; notes: Optional[str] = ""

class VisitBookResponse(BaseModel):
    visit_id: str; status: str; scheduled_date: datetime; message: str
    conflict: bool = False

class VisitOut(BaseModel):
    id: str; buyer_name: str; buyer_phone: str; buyer_email: str
    property_name: str; scheduled_date: datetime; end_time: Optional[datetime]
    status: str; assigned_agent: Optional[str]; agent_name: str
    feedback: str; rating: Optional[int]; notes: str
    postpone_reason: str; customer_id: Optional[str]
    created_at: datetime; updated_at: datetime
    class Config: from_attributes = True

class PostponeRequest(BaseModel):
    new_date: str; new_time: str; reason: str

class VisitFeedback(BaseModel):
    feedback: str; rating: int

class EnquiryCreate(BaseModel):
    buyer_name: str; buyer_phone: str; buyer_email: Optional[str] = ""
    source: str = "website"; property_interest: Optional[str] = ""
    budget_range: Optional[str] = ""; notes: Optional[str] = ""

class EnquiryUpdate(BaseModel):
    status: Optional[str] = None; assigned_to: Optional[str] = None
    notes: Optional[str] = None; priority: Optional[str] = None

class EnquiryOut(BaseModel):
    id: str; buyer_name: str; buyer_phone: str; buyer_email: str
    source: str; status: str; property_interest: str; budget_range: str
    notes: str; assigned_to: Optional[str]; priority: str; message_count: int
    last_agent_message: str; customer_id: Optional[str]
    created_at: datetime; updated_at: datetime
    class Config: from_attributes = True

class PropertyCreate(BaseModel):
    name: str; project_name: str; property_type: str; total_area_sqft: int = 0
    price_usd: int = 0; bedrooms: int = 3; bathrooms: int = 2
    floor_number: Optional[int] = None; total_floors: int = 0; facing: str = ""
    parking: int = 1; amenities: str = ""; completion_date: str = ""
    description: str = ""; location: str = ""; address: str = ""
    city: str = ""; state: str = ""; country: str = "USA"
    zip_code: str = ""; mls_id: str = ""; year_built: int = 2024
    lot_size_sqft: int = 0; hoa_monthly: int = 0

class PropertyOut(BaseModel):
    id: str; name: str; project_name: str; property_type: str
    total_area_sqft: int; price_usd: int; price_per_sqft: float
    bedrooms: int; bathrooms: int; floor_number: Optional[int]; total_floors: int
    facing: str; status: str; parking: int; amenities: str
    completion_date: str; description: str; location: str; address: str
    city: str; state: str; country: str; zip_code: str; mls_id: str
    year_built: int; lot_size_sqft: int; hoa_monthly: int
    class Config: from_attributes = True

class NotificationOut(BaseModel):
    id: str; title: str; body: str; category: str
    is_read: bool; link: str; created_at: datetime
    class Config: from_attributes = True
