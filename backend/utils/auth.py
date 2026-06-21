from datetime import datetime,timedelta
from typing import Optional,Dict,Any
from jose import JWTError,jwt
from passlib.context import CryptContext
from config import get_settings
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
settings = get_settings()


#password hashing
pwd_context =  CryptContext(schemes=["bcrypt"],deprecated = "auto")


security = HTTPBearer(auto_error=False)


# Authentication utility functions

def has_password (password:str) ->str:
    """Hash a password"""
    return pwd_context.hash(password)



def verify_password(plain_password:str,hash_password):
    return pwd_context.verify(plain_password,has_password)


def create_access_token (data:Dict[str,any],expires_delta:Optional[timedelta]=None)->str:
    """Create JWT access token"""
    to_encode =  data.copy()
    
    if expires_delta:
        expire =  datetime.utcnow() + expires_delta
    else:
        expire =  datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)
    return encoded_jwt
    
    
def create_refresh_token(data:Dict[str,any],expires_delta:Optional[timedelta])-> str:
    """Create JWT refresh token"""
    to_encode =  data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt =  jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)
    return encoded_jwt

    

def decode_token(token:str)-> Dict[str,Any]:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        user_id:int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate":"Bearer"}
            )
            
    except JWTError:
               raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate":"Bearer"}
            )


def verify_token_not_expired (token:str)-> bool :
    """Check if token is not expired"""
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        exp = payload.get("exp")
        return exp is None or exp >= datetime.utcnow().timestamp()
    
    except JWTError:
         return False


def get_current_user (credentials:HTTPAuthorizationCredentials = Depends(security),db:Session =  Depends(get_db)) -> User:
    """Return the currently authenticated user based on bearer token"""
    
    if not credentials or not credentials.credentials:
       raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload =  decode_token(credentials.credentials)
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user



