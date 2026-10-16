from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Backend settings. Read from environment variables or a local .env file."""

    model_config = SettingsConfigDict(env_prefix="AEROTWIN_", env_file=".env", extra="ignore")

    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
