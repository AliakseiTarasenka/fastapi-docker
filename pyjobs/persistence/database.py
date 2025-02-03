from sqlmodel import text
from sqlalchemy.ext.asyncio import create_async_engine
from pyjobs.persistence.config import Config

engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def initdb():
    """Create a connection to the database."""
    async with engine.begin() as conn:
        statement = text("select 'Hello World'")
        result = await conn.execute(statement)
        print(result.all())