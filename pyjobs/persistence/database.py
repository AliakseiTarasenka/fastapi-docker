from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from pyjobs.persistence.config import Config

engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))


async def initdb():
    """create a connection to the db"""

    async with engine.begin() as conn:
        statement = text("select 'Python developer'")

        result = await conn.execute(statement)

        print(result.all())