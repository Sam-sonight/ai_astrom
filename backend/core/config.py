# backend/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
import os
from pathlib import Path


class Settings(BaseSettings):
    # --- Application ---
    APP_NAME: str = Field("AI Astrom")
    ENVIRONMENT: str = Field("development")
    DEBUG: bool = Field(True)
    LOG_LEVEL: str = Field("INFO")

    # --- Paths ---
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"

    # --- Database ---
    DATABASE_URL: str = Field("sqlite:///./ai_astrom.db")

    # --- AI Provider ---
    AI_PROVIDER: str = Field("openai")
    OPENAI_API_KEY: str = Field(default="")
    AI_MODEL: str = Field("gpt-4o-mini")
    AI_TEMPERATURE: float = Field(0.7)
    AI_MAX_TOKENS: int = Field(800)

    # --- API Keys / Security ---
    JWT_SECRET_KEY: str = Field("secret")
    JWT_ALGORITHM: str = Field("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60)

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
