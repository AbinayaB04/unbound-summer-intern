from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AuditLog
from ..schemas import LogResponse
from ..auth import require_admin

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/", response_model=list[LogResponse])
def view_logs(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(AuditLog).all()

