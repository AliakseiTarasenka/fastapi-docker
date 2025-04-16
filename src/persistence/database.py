from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.persistence.config import Config
from src.models.books import Book
from src.models.user import User

# singleton connection to db
async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)


async def init_db():
    """Create async connection to the database.
    The usual way to issue CREATE is to use create_all() on the MetaData object.
    This method will issue queries that first check for the existence of each individual table,
    and if not found will issue the CREATE statements"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db():
    """Create async connection to the database. Drop all tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        yield session
