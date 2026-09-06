from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, chat, visits, enquiries
from app.routers.extra import properties_router, notifications_router, activity_router

settings = get_settings()
app = FastAPI(title=settings.app_name, version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(visits.router)
app.include_router(enquiries.router)
app.include_router(properties_router)
app.include_router(notifications_router)
app.include_router(activity_router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    from app.seed import seed; seed()

@app.get("/")
def root(): return {"app": settings.app_name, "version": "3.0.0", "status": "running"}

@app.get("/health")
def health(): return {"status": "healthy"}
