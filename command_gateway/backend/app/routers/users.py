from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse
from ..auth import require_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    api_key = uuid4().hex

    new_user = User(
        name=data.name,
        role=data.role,
        credits=data.credits,
        api_key=api_key,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(User).all()
