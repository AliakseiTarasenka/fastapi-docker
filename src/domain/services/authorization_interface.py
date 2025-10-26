from abc import ABC, abstractmethod
from typing import Iterable

from src.domain.models.users import User


class IRolePolicy(ABC):
    """
    Domain contract for evaluating whether a User
    has the rights to perform an action.
    """

    @abstractmethod
    def is_allowed(self, user: User) -> bool:
        """
        Return True if user is authorized according to the policy.
        """


class RoleBasedPolicy(IRolePolicy):
    """
    Policy that checks a user's role against allowed ones.
    """

    def __init__(self, allowed_roles: Iterable[str]):
        self._allowed_roles = set(allowed_roles)

    def is_allowed(self, user: User) -> bool:
        return user.role in self._allowed_roles
