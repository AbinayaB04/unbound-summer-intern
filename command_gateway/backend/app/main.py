from fastapi import FastAPI, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from .database import Base, engine, SessionLocal
from .routers import users, commands, rules, logs
from .models import User
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# create tables
Base.metadata.create_all(bind=engine)

# Seed admin
def seed_admin():
    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter(User.role == "admin").first()
        if not admin:
            api_key = uuid4().hex
            admin = User(name="admin", role="admin", credits=1000, api_key=api_key)
            db.add(admin)
            db.commit()
            print("\n=== ADMIN API KEY CREATED ===")
            print("Admin API Key:", api_key)
            print("=============================\n")
    finally:
        db.close()

seed_admin()

app = FastAPI(title="Command Gateway Backend")

# API key header for Swagger
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Dependency to get current user
def get_current_user(x_api_key: str = Security(api_key_header), db: Session = Depends(SessionLocal)):
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user

# Include routers
app.include_router(users.router)
app.include_router(commands.router)
app.include_router(rules.router)
app.include_router(logs.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, use ["http://127.0.0.1:5500"] for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"status": "Backend running"}
