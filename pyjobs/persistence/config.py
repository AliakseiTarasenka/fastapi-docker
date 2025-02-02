from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config(SettingsConfigDict):
        env_file = "../../.env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

Config = Settings()