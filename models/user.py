"""
User model definition.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

from config.database import Base

# SQLAlchemy ORM Model
class User(Base):
    """SQLAlchemy User model for database operations."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with Todo model
    todos = relationship("Todo", back_populates="user")

# OTP model for password reset
class OTPModel(Base):
    """SQLAlchemy OTP model for password reset operations."""
    __tablename__ = "otps"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), index=True, nullable=False)
    otp = Column(String(6), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)

# Pydantic Models for API request/response
class UserBase(BaseModel):
    """Base Pydantic model for User with common attributes."""
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """Pydantic model for creating a new User."""
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    """Pydantic model for User login."""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """Pydantic model for User response."""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    """Pydantic model for token response."""
    access_token: str
    token_type: str

class ForgotPassword(BaseModel):
    """Pydantic model for forgot password request."""
    email: EmailStr

class VerifyOTP(BaseModel):
    """Pydantic model for OTP verification."""
    email: EmailStr
    otp: str

class ResetPassword(BaseModel):
    """Pydantic model for password reset."""
    email: EmailStr
    otp: str
    new_password: str = Field(..., min_length=8)
