from typing import Generic,List,TypeVar,Dict
from config import get_settings
from pydantic import BaseModel
from sqlalchemy.orm import Query

settings = get_settings()

T = TypeVar('T')


class PaginatedResponse(BaseModel,Generic[T]):
    """Generic paginated response"""
    items : List[T]
    total:int
    page:int
    page_size:int
    total_pages:int
    has_next:bool
    has_prev:bool

def paginate_query(query:Query,page:int=1,page_size:int=None)->tuple[Query,int]:
    """Apply pagination to a query"""
    
    if page_size is None:
        page_size = settings.default_page_size
    
    #Ensure page_size is within limits
    page_size = min(page_size,settings.max_page_size)
    page_size = max(page_size,1)
    
    # Ensure page is at least 1
    page =  max(page,1)
    
    #Get total count
    total = query.count()
    
    #Apply offset  and limit
    offset = (page-1)*page_size
    query = query.offset(offset).limit(page_size)
    
    return query,total
    

def create_paginated_response (items:List[T],total:int,page:int,page_size:int)-> Dict[str,any]:
    """Create a paginated response"""
    total_pages = (total+page_size-1)//page_size
    
    return {
        "items":items,
        "total":total,
        "page":page,
        "page_size":page_size,
        "total_pages":total_pages,
        "has_next":page<total_pages,
        "has_prev":page>1
    }