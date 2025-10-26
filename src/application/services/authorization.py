from typing import Optional

from src.application.errors import InsufficientPermission
from src.domain.models.users import User
from src.domain.services.authorization_interface import IRolePolicy


class AuthorizationService:
    """
    Application-layer service that enforces authorization rules
    using a domain-defined policy.
    """

    def __init__(self, policy: IRolePolicy):
        self.policy = policy

    def check_access(self, user: User) -> Optional[bool]:
        if not self.policy.is_allowed(user):
            raise InsufficientPermission()
        return True
