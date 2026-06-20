import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings (BaseSettings):
     # App
    app_name: str = "E-Commerce API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:password@localhost/ecommerce_db"
    # For local development: sqlite:///./ecommerce.db
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Email
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    email_from: str = "noreply@ecommerce.com"
    email_password: str = ""
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Payment Gateways
    stripe_api_key: str = ""
    stripe_webhook_secret: str = ""
    sslcommerz_store_id: str = ""
    sslcommerz_store_password: str = ""
    sslcommerz_sandbox: bool = True
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    class config:
        env_file=".env"
        case_sensitive = False
        

@lru_cache
def get_settings():
    return  Settings()