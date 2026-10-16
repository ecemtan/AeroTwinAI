from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.aircraft_registry import project_root


class Settings(BaseSettings):
    """Backend settings. Read from environment variables or the repository .env file."""

    model_config = SettingsConfigDict(
        env_prefix="AEROTWIN_", env_file=project_root() / ".env", extra="ignore"
    )

    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
