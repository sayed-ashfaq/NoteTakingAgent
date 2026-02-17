
import os
from typing import List, Union
from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Note Taker API"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    DATABASE_URL: str = "sqlite:///./data/app.db"

    # Authentication (Clerk)
    CLERK_SECRET_KEY: str
    CLERK_PUBLISHABLE_KEY: str
    CLERK_ISSUER: str = "" # Optional, usually specific to instance

    # AI Models
    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    
    # Optional: Open Source Model Endpoint
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
