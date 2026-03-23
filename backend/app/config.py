"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "dungeon-tycoon-llm"
    app_env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000

    # LLM backend: "ollama" or "anthropic"
    llm_backend: str = Field(default="ollama", alias="LLM_BACKEND")

    # Ollama (default — local, free)
    ollama_base_url: str = Field(default="http://localhost:11434/v1", alias="OLLAMA_BASE_URL")
    ollama_primary_model: str = Field(default="mistral", alias="OLLAMA_PRIMARY_MODEL")
    ollama_fast_model: str = Field(default="mistral", alias="OLLAMA_FAST_MODEL")

    # Anthropic (optional — cloud, paid)
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
