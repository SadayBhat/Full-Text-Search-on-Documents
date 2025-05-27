import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  
    # Application info
    APP_NAME: str = "FastAPI Text Search"
    APP_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # File storage
    UPLOAD_DIR: str = "uploads"
    
    # API settings
    API_PREFIX: str = "/api/v1"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]
    
    # Environment-specific settings
    ENV: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Load settings
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
