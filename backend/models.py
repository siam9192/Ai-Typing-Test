from database import Base
from sqlalchemy import Column,Integer,String,Boolean,DateTime,Index,JSON,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Index
)
from sqlalchemy.orm import relationship
import enum

class TestMode (str,enum.Enum):
    TEST = "test"
    COMPETITIVE = "competitive"
    

class TestLevel(str,enum.Enum):
    EASY = "easy",
    MEDIUM = "medium"
    EXPERT = "expert"
    


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String(50), nullable=False)
    hashed_password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    last_login = Column(DateTime)
    
    leaderboard_ranking = Column(Integer,nullable=False)
    total_score = Column(Integer,default=0,nullable=False)
    highest_score = Column(Integer,default=0,nullable=False) 
    highest_wpm = Column(Integer,default=0,nullable=False)
    participation_count = Column(Integer,default=0,nullable=False)
    test_level = Column(Enum(TestLevel),nullable=True)
    
    # Relationships
    tests = relationship(
        "Test",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_user_email", "email"),
    )


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True,autoincrement=True)
    wpm = Column(Integer, nullable=False)
    cpm = Column(Integer, nullable=False)
    error_count = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)
    time_sec = Column(Integer, nullable=False)

    progress_tracking = Column(JSON, nullable=False)
    score_summary = Column(JSON, nullable=False)

    total_score = Column(Integer, nullable=False)
    
    ai_suggestion = Column(String(10000),nullable=False)
    
    mode = Column(Enum(TestMode),nullable=False)
   
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    
    created_at = Column(DateTime,default=datetime.utcnow,index=True)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    # Relationship
    user = relationship(
        "User",
        back_populates="tests"
    )
    


    
