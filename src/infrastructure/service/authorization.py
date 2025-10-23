from typing import Any, List

from fastapi import Depends

from src.domain.models.users import User
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.persistence.users_repository import UserRepository
from src.infrastructure.service.authentication import AccessTokenBearer
from src.infrastructure.service.errors import InsufficientPermission


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    user_repository: UserRepository = Depends(get_user_repository),
):
    user_email = token_details["user"]["email"]

    user = await user_repository.get_user_by_email(user_email)

    return user


class RoleChecker:
    """
    Role Based Access Control Class. Checks whether a user is in an allowed role list
    """

    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        """ "
        Making class callable
        Verify that the user has role allowed to access specific endpoints
        and email address is verified
        """
        # if not current_user.is_verified:
        #     raise AccountNotVerified()

        if current_user.role not in self.allowed_roles:
            raise InsufficientPermission()

        return True
