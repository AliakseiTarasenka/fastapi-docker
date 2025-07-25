from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from persistence.config import Config

# singleton connection to db
async_engine = create_async_engine(url=Config.database_url, echo=True)


async def init_db():
    """Create async connection to the database.

    The usual way to issue CREATE is to use create_all() on the MetaData
    object. This method will issue queries that first check for the
    existence of each table, and if a table is not found, it will issue
    the CREATE statements
    """
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def drop_db():
    """Create async connection to the database.

    Drop all tables
    """
    async with async_engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)


async def get_session() -> AsyncSession:
    session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as session:
        yield session
