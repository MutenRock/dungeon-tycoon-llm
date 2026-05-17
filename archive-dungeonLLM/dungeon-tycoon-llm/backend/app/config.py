from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="Dungeon Tycoon LLM", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    host: str = Field(default="127.0.0.1", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    save_dir: str = Field(default="./saves", alias="SAVE_DIR")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


settings = Settings()
