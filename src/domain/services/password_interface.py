from abc import ABC, abstractmethod


class IPasswordService(ABC):
    """Abstract interface for password service"""

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError()
