from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.application.services.reviews import ReviewService
from src.domain.repositories.book_repository_interface import IBookRepository
from src.domain.repositories.reviews_repository_interface import IReviewRepository
from src.domain.repositories.tags_repository_interface import ITagRepository
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.services.password_interface import IPasswordService
from src.infrastructure.database.database import get_session
from src.infrastructure.dependencies.services import get_password_service
from src.infrastructure.repositories.books_repository import BookRepository
from src.infrastructure.repositories.reviews_repository import ReviewRepository
from src.infrastructure.repositories.tags_repository import TagRepository
from src.infrastructure.repositories.users_repository import UserRepository


async def get_user_repository(
    session: AsyncSession = Depends(get_session),
    password_service: IPasswordService = Depends(get_password_service),
) -> IUserRepository:
    return UserRepository(session, password_service)


async def get_book_repository(
    session: AsyncSession = Depends(get_session),
) -> IBookRepository:
    return BookRepository(session)


async def get_review_repository(
    session: AsyncSession = Depends(get_session),
) -> IReviewRepository:
    return ReviewRepository(session)


async def get_review_service(
    review_repository: IReviewRepository = Depends(get_review_repository),
    user_repository: IUserRepository = Depends(get_user_repository),
    book_repository: IBookRepository = Depends(get_book_repository),
) -> ReviewService:
    return ReviewService(review_repository, user_repository, book_repository)


async def get_tags_repository(
    session: AsyncSession = Depends(get_session),
) -> ITagRepository:
    return TagRepository(session)
