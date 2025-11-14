from typing import Tuple

from src.domain.models.users import User
from src.domain.services.authentication_interface import IAuthenticationService


class Authentication(IAuthenticationService):

    def __init__(self):
        pass

    async def authenticate_user(self, email: str, password: str) -> Tuple[User, str, str]:
        """Authenticate user and return user, access_token, refresh_token"""
        pass

    async def verify_token_data(self, token: str) -> None:
        """Validate JWT token and return token data"""
        pass

    async def revoke_token(self, jti: str) -> None:
        """Revoke a token by JTI"""
        pass
