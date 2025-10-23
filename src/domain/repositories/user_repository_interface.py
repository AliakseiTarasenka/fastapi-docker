from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.users import User
from src.presentation.web.schemas.users import UserCreateModel


class IUserRepository(ABC):
    """Interface for user repository operations"""

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email"""

    @abstractmethod
    async def user_exists(self, email: str) -> bool:
        """Check if a user exists by email"""

    @abstractmethod
    async def create_user(self, user_data: UserCreateModel) -> User:
        """Create a new user"""

    @abstractmethod
    async def delete_user(self, email: str) -> bool:
        """Delete a user by email"""
