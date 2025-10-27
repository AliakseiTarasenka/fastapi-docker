from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.repositories.book_repository_interface import IBookRepository
from src.domain.repositories.user_repository_interface import IUserRepository
from src.infrastructure.database.database import get_session
from src.infrastructure.repositories.books_repository import BookRepository
from src.infrastructure.repositories.users_repository import UserRepository
from src.infrastructure.service.auth.password_management import PasswordService


async def get_user_repository(
    session: AsyncSession = Depends(get_session),
    password_service: PasswordService = Depends(PasswordService),
) -> IUserRepository:
    return UserRepository(session, password_service)


async def get_book_repository(
    session: AsyncSession = Depends(get_session),
) -> IBookRepository:
    return BookRepository(session)
