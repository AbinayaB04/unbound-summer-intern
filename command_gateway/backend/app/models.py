from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="member")  # admin/member
    credits = Column(Integer, default=0)

    commands = relationship("Command", back_populates="user")
    logs = relationship("AuditLog", back_populates="user")


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    command_text = Column(Text, nullable=False)
    status = Column(String)  # executed, rejected, pending
    credits_used = Column(Integer, default=0)
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="commands")


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    pattern = Column(String, nullable=False)
    action = Column(String, nullable=False)  # AUTO_ACCEPT, AUTO_REJECT, REQUIRE_APPROVAL
    created_at = Column(DateTime, server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    command_text = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="logs")

