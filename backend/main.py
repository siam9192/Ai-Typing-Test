from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
# from database import Base,engine



settings =  get_settings()


app =  FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials= True,
    allow_methods = ["*"] ,
    allow_headers = ["*"]        
    )



@app.on_event("startup")
def startup_event():
    # Base.metadata.create_all(bind=engine)
    pass
   
@app.get("/")
def root():
    return {
        "message":"App is running"
    }