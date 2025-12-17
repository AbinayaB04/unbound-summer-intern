import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Rule

from ..schemas import RuleCreate, RuleResponse
from ..auth import require_admin

router = APIRouter(prefix="/rules", tags=["Rules"])

@router.post("/", response_model=RuleResponse)
def add_rule(data: RuleCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    # 1️⃣ Check duplicate pattern
    existing = db.query(Rule).filter(Rule.pattern == data.pattern).first()
    if existing:
        raise HTTPException(status_code=400, detail="Rule pattern already exists!")

    # 2️⃣ Validate regex
    try:
        re.compile(data.pattern)
    except re.error:
        raise HTTPException(status_code=400, detail="Invalid regex pattern")

    # 3️⃣ Add new rule
    rule = Rule(pattern=data.pattern, action=data.action)
    db.add(rule)
    db.commit()
    db.refresh(rule)
    # inside POST /rules/

    return rule

@router.get("/", response_model=list[RuleResponse])
def list_rules(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Rule).all()
