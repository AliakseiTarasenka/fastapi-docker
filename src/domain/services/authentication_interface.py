from abc import ABC, abstractmethod
from typing import Tuple

from src.domain.models.users import User


class AuthenticationService(ABC):
    @abstractmethod
    async def authenticate_user(self, email: str, password: str) -> Tuple[User, str, str]:
        """Authenticate user and return user, access_token, refresh_token"""
        pass

    @abstractmethod
    async def validate_token(self, token: str) -> dict:
        """Validate JWT token and return token data"""
        pass

    @abstractmethod
    async def revoke_token(self, jti: str) -> None:
        """Revoke a token by JTI"""
        pass
