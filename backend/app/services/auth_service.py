from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.config import get_settings
from app.models import User
from app.schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()

def hash_password(p: str) -> str: return pwd_context.hash(p)
def verify_password(plain: str, hashed: str) -> bool: return pwd_context.verify(plain, hashed)

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    u = db.query(User).filter(User.email == email).first()
    if not u or not verify_password(password, u.hashed_password): return None
    return u if u.is_active else None

def create_token(user: User) -> str:
    return jwt.encode({"sub": user.id, "email": user.email, "name": user.full_name, "role": user.role,
                        "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)},
                       settings.secret_key, algorithm=settings.algorithm)

def verify_token(token: str) -> Optional[TokenData]:
    try:
        p = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return TokenData(sub=p["sub"], name=p["name"], role=p["role"])
    except JWTError: return None
