"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "dungeon-tycoon-llm"
    app_env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000

    # Anthropic LLM
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    anthropic_primary_model: str = Field(
        default="claude-sonnet-4-20250514", alias="ANTHROPIC_PRIMARY_MODEL"
    )
    anthropic_fast_model: str = Field(
        default="claude-haiku-4-5-20251001", alias="ANTHROPIC_FAST_MODEL"
    )
    llm_primary_timeout: int = 10000  # ms
    llm_fast_timeout: int = 3000  # ms
    llm_fallback_enabled: bool = True

    # Persistence
    save_dir: str = "./saves"

    # Localisation
    default_language: str = "en"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
