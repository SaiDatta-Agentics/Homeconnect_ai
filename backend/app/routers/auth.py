import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, LoginResponse, UserOut, RegisterRequest
from app.services.auth_service import authenticate, create_token, verify_token, hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    td = verify_token(cred.credentials)
    if not td: raise HTTPException(401, "Invalid or expired token")
    u = db.query(User).filter(User.id == td.sub).first()
    if not u or not u.is_active: raise HTTPException(401, "User not found")
    return u

def require_admin(u: User = Depends(get_current_user)) -> User:
    if u.role not in ("admin", "sales_manager", "sales_agent"):
        raise HTTPException(403, "Admin access required")
    return u

@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    u = authenticate(db, body.email, body.password)
    if not u: raise HTTPException(401, "Invalid email or password")
    return LoginResponse(access_token=create_token(u), user=UserOut.model_validate(u))

@router.post("/register", response_model=LoginResponse)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already registered")
    u = User(id=str(uuid.uuid4()), email=body.email, hashed_password=hash_password(body.password),
             full_name=body.full_name, phone=body.phone, role="customer")
    db.add(u); db.commit(); db.refresh(u)
    return LoginResponse(access_token=create_token(u), user=UserOut.model_validate(u))

@router.get("/me", response_model=UserOut)
def me(u: User = Depends(get_current_user)):
    return UserOut.model_validate(u)
