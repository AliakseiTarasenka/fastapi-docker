from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# BaseSettings class is used for loading environment variables to the Settings class
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JTI_EXPIRY: int
    REDIS_URL: str
    ENVIRONMENT: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = False
    DOMAIN: str
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        extra="ignore",  # ignore extra .env variables from being read
    )


Config = Settings()
