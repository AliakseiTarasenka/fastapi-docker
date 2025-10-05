from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# BaseSettings class is used for loading environment variables to the Settings class
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",  # ignore extra .env variables from being read
    )


Config = Settings()
