from abc import ABC, abstractmethod

from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.users import User
from src.domain.services.password_interface import IPasswordService
from src.presentation.web.schemas.users import UserCreateModel


class IUserRepository(ABC):
    """Interface for user repository operations"""

    @abstractmethod
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        """Fetch a user by email"""

    @abstractmethod
    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        """Check if a user exists by email"""

    @abstractmethod
    async def create_user(
        self, user_data: UserCreateModel, session: AsyncSession, password_service: IPasswordService
    ) -> User:
        """Create a new user"""

    @abstractmethod
    async def delete_user(self, email: str, session: AsyncSession) -> bool:
        """Delete a user by email"""

    @abstractmethod
    async def update_user(self, user: User, user_data: dict, session: AsyncSession) -> User:
        """Update a user data"""
