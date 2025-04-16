from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
# import os

class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore"
    )

# os.environ['DATABASE_URL'] = 'postgresql+asyncpg://neondb_owner:npg_f0LFVabRWD1p@ep-weathered-rice-a55x6kmv-pooler.us-east-2.aws.neon.tech/neondb'
# print("DEBUG: DATABASE_URL from env:", os.getenv("DATABASE_URL"))

Config = Settings()