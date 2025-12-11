from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import User


def get_current_user(
    api_key: str = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db),
):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    user = db.query(User).filter(User.api_key == api_key).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user


def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
