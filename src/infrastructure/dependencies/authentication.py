from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.application.errors import UserNotFound
from src.domain.repositories.user_repository_interface import IUserRepository
from src.infrastructure.dependencies.database import get_session
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.service.auth.token_bearer import AccessTokenBearer

access_security_scheme = AccessTokenBearer()


# Return current user
async def get_current_user(
    token_data: dict = Depends(access_security_scheme),
    user_repository: IUserRepository = Depends(get_user_repository),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_data["user"]["email"]
    user = await user_repository.get_user_by_email(user_email, session)
    if not user:
        raise UserNotFound()
    return user
