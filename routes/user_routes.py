"""
Routes for User operations including registration, login, and password reset.
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import random
import string

from config.database import get_db
from models.user import (
    Test, User, UserCreate, UserResponse, TokenResponse, 
    ForgotPassword, VerifyOTP, ResetPassword, OTPModel
)
from utils.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user
)
from utils.email import send_otp_email

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if email already exists
    db_user_email = db.query(User).filter(User.email == user.email).first()
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    db_user_username = db.query(User).filter(User.username == user.username).first()
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed due to database error"
        )

@router.post("/login", response_model=TokenResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login a user and return an access token."""
    # Find user by email (username field in form is actually the email)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    """Get information about the current logged-in user."""
    return current_user

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(
    request: ForgotPassword,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate and send an OTP for password reset."""
    # Check if user exists
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # We don't want to reveal if an email exists or not for security reasons
        return {"message": "If your email is registered, you will receive an OTP"}
    
    # Generate a 6-digit OTP
    otp = ''.join(random.choices(string.digits, k=6))
    
    # Set expiration time (15 minutes from now)
    expiry_time = datetime.utcnow() + timedelta(minutes=15)
    
    # Delete any existing OTPs for this email
    db.query(OTPModel).filter(OTPModel.email == request.email).delete()
    
    # Save the OTP in the database
    db_otp = OTPModel(
        email=request.email,
        otp=otp,
        expires_at=expiry_time
    )
    
    db.add(db_otp)
    db.commit()
    
    # Send OTP email in the background
    background_tasks.add_task(
        send_otp_email,
        recipient_email=request.email,
        otp=otp
    )
    
    return {"message": "If your email is registered, you will receive an OTP"}

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(request: VerifyOTP, db: Session = Depends(get_db)):
    """Verify an OTP for password reset."""
    # Find the OTP record
    otp_record = db.query(OTPModel).filter(
        OTPModel.email == request.email,
        OTPModel.otp == request.otp,
        OTPModel.is_used == False,
        OTPModel.expires_at > datetime.utcnow()
    ).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    return {"message": "OTP verified successfully"}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(request: ResetPassword, db: Session = Depends(get_db)):
    """Reset a user's password using a verified OTP."""
    # Find the OTP record
    otp_record = db.query(OTPModel).filter(
        OTPModel.email == request.email,
        OTPModel.otp == request.otp,
        OTPModel.is_used == False,
        OTPModel.expires_at > datetime.utcnow()
    ).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Find the user
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    
    # Mark OTP as used
    otp_record.is_used = True
    
    # Commit changes
    db.commit()
    
    return {"message": "Password reset successfully"}

@router.get("/test/{id}", response_model=Test)
def get_test(id: int):
    """Test endpoint to demonstrate schema usage.
    
    This shows how a Pydantic schema controls both input validation and response formatting.
    The schema definition in models/user.py determines what fields are returned and their types.
    
    Args:
        id: A test ID to include in the response
        
    Returns:
        A Test object with the provided ID, a test name, and default is_active value
    """
    # Create a Test object with the provided ID and some default values
    # FastAPI will validate this against the Test schema and format the response accordingly
    return Test(id=id, name="Test Item")
