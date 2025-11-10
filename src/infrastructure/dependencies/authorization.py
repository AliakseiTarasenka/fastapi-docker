from fastapi import Depends

from src.application.errors import InsufficientPermission
from src.application.services.authorization import AuthorizationService
from src.domain.models.users import User
from src.domain.services.authorization_interface import RoleBasedPolicy
from src.infrastructure.dependencies.authentication import get_current_user


def get_role_checker(allowed_roles: list[str]):
    """
    Dependency factory that creates a role checker dependency
    for specific endpoint access control rules.
    """

    policy = RoleBasedPolicy(allowed_roles)
    auth_service = AuthorizationService(policy)

    def checker(current_user: User = Depends(get_current_user)):
        try:
            auth_service.check_access(current_user)
        except InsufficientPermission as e:
            raise InsufficientPermission()
        return True

    return checker
