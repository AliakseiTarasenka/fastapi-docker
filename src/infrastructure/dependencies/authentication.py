from fastapi import Depends, Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain.repositories.user_repository_interface import IUserRepository
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.service.auth.token_bearer import AccessTokenBearer
from src.infrastructure.service.auth.token_bearer import RefreshTokenBearer
from src.infrastructure.service.auth.token_management import TokenService

access_security_scheme = HTTPBearer(description="Provide a valid access token as 'Bearer <token>'")


def get_token_service() -> TokenService:
    """Provide TokenService instance for dependency injection."""
    return TokenService()


def get_access_token_bearer() -> AccessTokenBearer:
    return AccessTokenBearer()


def get_refresh_token_bearer() -> RefreshTokenBearer:
    """Provide RefreshTokenBearer instance with injected dependencies."""
    return RefreshTokenBearer()


async def get_access_token(
    credentials: HTTPAuthorizationCredentials = Security(access_security_scheme),
    token_service: TokenService = Depends(get_token_service),
):
    token = credentials.credentials
    token_data = token_service.decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token",
        )
    return token_data


# Return current user
async def get_current_user(
    token_data: dict = Security(get_access_token),
    user_repository: IUserRepository = Depends(get_user_repository),
):
    user_email = token_data["user"]["email"]
    user = await user_repository.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
