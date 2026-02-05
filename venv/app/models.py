import uuid
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    __tablename__ = "roles"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(String(36), ForeignKey("roles.id"))
    created_at = Column(DateTime, server_default=func.now())

    role = relationship("Role")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    status = Column(Enum("pending", "in_progress", "completed"), default="pending")
    priority = Column(Enum("low", "medium", "high"), default="medium")
    owner_id = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    owner = relationship("User")
