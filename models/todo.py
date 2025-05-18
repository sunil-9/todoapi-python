"""
Todo model definition.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from config.database import Base

# SQLAlchemy ORM Model
class Todo(Base):
    """SQLAlchemy Todo model for database operations."""
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship with User model
    user = relationship("User", back_populates="todos")

# Pydantic Models for API request/response
class TodoBase(BaseModel):
    """Base Pydantic model for Todo with common attributes."""
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TodoCreate(TodoBase):
    """Pydantic model for creating a new Todo."""
    pass

class TodoUpdate(BaseModel):
    """Pydantic model for updating an existing Todo."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(TodoBase):
    """Pydantic model for Todo response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    
    class Config:
        orm_mode = True
