from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from database import Base,engine
from routes.auth import router as auth_router


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


app.include_router(auth_router)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    
   
@app.get("/")
def root():
    return {
        "message":"App is running"
    }