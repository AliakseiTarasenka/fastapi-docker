from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from pyjobs.persistence.config import Config

engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def initdb():
    """Create async connection to the database."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)