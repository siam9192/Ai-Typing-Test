from pydantic import BaseModel,EmailStr,Field,Json
from typing import Optional,List,Dict,Any
from datetime import datetime
from models import TestMode,TestLevel

class UserRegister(BaseModel):
    email:EmailStr
    full_name:str = Field(...,min_length=3,max_length=100)
    password: str = Field(..., min_length=8)
    
    

class UserResponse(BaseModel):
    id:int
    email:str
    full_name:str
    profile_picture:Optional[str]
    
    
    is_active:bool
    created_at:datetime
    updated_at:datetime
    last_login:Optional[datetime]
    
    leaderboard_ranking:int
    total_score:int
    highest_score:int
    highest_wpm:int
    participation_count:int
    
    class config:
        from_attributes = True


class UserLogin (BaseModel):
    email:EmailStr
    password:str
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
     refresh_token: str
  
  
class TestData(BaseModel):
    wpm: int
    cpm: int
    error_count: int
    accuracy: int
    time_sec: int
    progress_tracking: Dict[str, Any]
    mode: TestMode
    level: TestLevel
    

class TestResponse (BaseModel):
    id:int
    wpm:int
    cpm:int
    error_count:int
    accuracy:int
    time_sec:int

    progress_tracking:Dict[str,any]
    score_summary:Dict[str,any]
    total_score:int
    ai_suggestion:str
    mode:TestMode
    user_id:int
    created_at:datetime
    updated_at:datetime
    
    class config:
        from_attributes = True