from fastapi import Depends, HTTPException, status

from src.domain.repositories.user_repository_interface import IUserRepository
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.service.auth.token_bearer import AccessTokenBearer

access_security_scheme = AccessTokenBearer()


# Return current user
async def get_current_user(
    token_data: dict = Depends(access_security_scheme),
    user_repository: IUserRepository = Depends(get_user_repository),
):
    user_email = token_data["user"]["email"]
    user = await user_repository.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
