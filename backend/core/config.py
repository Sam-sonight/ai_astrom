# backend/core/config.py
from __future__ import annotations

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application configuration using Pydantic v2 + pydantic-settings.
    All other modules should only read values from this class.
    """

    # ------------------------------------------------------------------
    # App / runtime
    # ------------------------------------------------------------------
    APP_NAME: str = Field(default="AI Astrom API")
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")

    # ------------------------------------------------------------------
    # Paths / data
    # ------------------------------------------------------------------
    # Base directory where interpretation text, templates, etc. live.
    # horoscope_service.py expects DATA_DIR to exist.
    DATA_DIR: str = Field(default="data")

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    # Example: "sqlite:///./ai_astrom.db" or a full Postgres URL
    DATABASE_URL: str = Field(default="sqlite:///./ai_astrom.db")

    # ------------------------------------------------------------------
    # AI configuration
    # ------------------------------------------------------------------
    AI_PROVIDER: str = Field(default="local")          # "local" or "openai"
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL: str = Field(default="gpt-4o-mini")
    AI_TEMPERATURE: float = Field(default=0.7)
    AI_MAX_TOKENS: int = Field(default=800)

    # ------------------------------------------------------------------
    # Security / JWT
    # ------------------------------------------------------------------
    # Internal canonical names
    SECRET_KEY: str = Field(default="change-me-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)

    # Backwards-compatibility aliases expected by core/security.py
    JWT_SECRET_KEY: str = Field(default="change-me-in-production")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    # Comma-separated origins string, e.g. "http://localhost:3000,https://myapp.com"
    BACKEND_CORS_ORIGINS: Optional[str] = None

    # ------------------------------------------------------------------
    # Pydantic v2 Settings config
    # ------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unknown env vars instead of raising
    )


# Singleton settings instance
settings = Settings()
