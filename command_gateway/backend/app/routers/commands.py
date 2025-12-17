import re
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Command, Rule, AuditLog
from ..schemas import CommandCreate, CommandResponse
from ..utils.credit_manager import deduct_credit
from ..auth import get_current_user

router = APIRouter(prefix="/commands", tags=["Commands"])


@router.post("/", response_model=CommandResponse)
def submit_command(
    data: CommandCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    # 0️⃣ Check user credits
    if user.credits <= 0:
        new_cmd = Command(
            user_id=user.id,
            command_text=data.command_text,
            status="rejected",
            credits_used=0
        )
        db.add(new_cmd)
        db.commit()
        db.refresh(new_cmd)

        # Log rejection
        log = AuditLog(
            user_id=user.id,
            action="rejected",
            command_text=data.command_text
        )
        db.add(log)
        db.commit()

        return new_cmd

    cmd = data.command_text

    # 1️⃣ Find matching rule
    rules = db.query(Rule).all()
    matched_action = None
    for rule in rules:
        if re.search(rule.pattern, cmd):
            matched_action = rule.action
            break

    status = "pending"

    # 2️⃣ Handle rule actions
    if matched_action == "AUTO_REJECT":
        status = "rejected"
        deduct_credit(user, db)  # Deduct 1 credit for rejected command

    elif matched_action == "AUTO_ACCEPT":
        if deduct_credit(user, db):
            status = "executed"
        else:
            status = "rejected"

    elif matched_action == "REQUIRE_APPROVAL":
        status = "pending"

    # 3️⃣ Save command
    new_cmd = Command(
        user_id=user.id,
        command_text=cmd,
        status=status,
        credits_used=1 if status in ["executed"] else 0,
    )
    db.add(new_cmd)
    db.commit()
    db.refresh(new_cmd)

    # 4️⃣ Log action
    log = AuditLog(
        user_id=user.id,
        action=status,
        command_text=cmd
    )
    db.add(log)
    db.commit()

    return new_cmd





@router.get("/", response_model=list[CommandResponse])
def list_user_commands(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Command).filter(Command.user_id == user.id).all()
