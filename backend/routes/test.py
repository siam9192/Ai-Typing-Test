from fastapi import APIRouter,Depends,Query
from models import Test,User,TestMode,TestLevel
from database import get_db
from schemas import TestData,TestResponse
from sqlalchemy.orm import Session
from utils.auth import get_current_user
from typing import List
from utils.helper import paginate_query,create_paginated_response,PaginatedResponse
router = APIRouter(prefix="/api/v1/tests",tags=["Tests"])

@router.post("/")
def create_test(test_data=TestData,current_user:User=Depends(get_current_user),db:Session = Depends(get_db)):
      
 if current_user is not None:
    test = Test(
    wpm=test_data.wpm,
    cpm =  test_data.cpm,
    error_count = test_data.error_count,
    accuracy = test_data.accuracy,
    time_sec = test_data.time_sec,
    progress_tracking = test_data.progress_tracking,
    score_summary = test_data.score_summary,
    mode = test_data.mode,
    user_id = current_user.id
    )
    
    if test_data.level:
        test.level = test_data.level
    
    if test_data.mode == TestMode.TEST:
      speed_score = test_data.wpm * 2
      accuracy_score = test_data.accuracy * 5
      error_penalty = test_data.error_count * 3
      
      total_score = max(
      0,
      speed_score + accuracy_score - error_penalty
      )
    
      test.total_score = total_score
      test.score_summary = {
        "speed_score":speed_score,
        "accuracy_score":accuracy_score,
        "error_penalty":error_penalty,
      }
      
    
    
@router.get("/",response_model=PaginatedResponse)
def get_tests(current_user:User = Depends(get_current_user),db:Session = Depends(get_db),page:int = Query(1,ge=1),limit= Query(10,ge=0,le=100),mode:str=Query(None),order_by:str = Query(None)):
  """Get user tests"""
  query = db.query(Test).filter(User.id ==  current_user.id)
  
  if mode:
    query = query.filter(Test.mode == mode)
  
  if not order_by:
    query.order_by(Test.created_at.desc())
  
  query,total = paginate_query(query,page=page,page_size=limit)
  
  tests = query.all()
  
  return create_paginated_response([TestResponse.from_orm(o) for o in tests],total,page,limit)