from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserRegister,UserResponse,UserLogin,TokenResponse,TokenRefresh
from utils.auth import hash_password,verify_password,create_access_token,create_refresh_token,decode_token
from datetime import datetime

router = APIRouter(prefix="/api/v1/auth",tags=["authentication"])

@router.post("/register",response_model=UserResponse)
def register(user_data:UserRegister,db:Session = Depends(get_db)):
    """Register a new user"""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email  already exists"
        )
    
    user = User (
        email = user_data.email,
        full_name = user_data.full_name,
        hashed_password = hash_password(user_data.password),
        leaderboard_ranking = 0
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user



@router.post("/login",response_model=TokenResponse)
def login (credentials:UserLogin,db=Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    user.last_login = datetime.utcnow()
    db.commit()

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id,type:"refresh"})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
  
@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """Refresh tokens using a valid refresh token"""
    payload = decode_token(token_data.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )

    return {
        "access_token": create_access_token({"sub": user.id}),
        "refresh_token": create_refresh_token({"sub": user.id}),
        "token_type": "bearer"
    }


