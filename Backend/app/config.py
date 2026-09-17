import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./agrismart.db"
    WEATHER_API_KEY: str = ""
    AI_API_KEY: str = ""
    AI_PROVIDER: str = "gemini"
    FRONTEND_URL: str = "http://localhost:3000"
    DISEASE_AI_MODE: str = "demo"
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)