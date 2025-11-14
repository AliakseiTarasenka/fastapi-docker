from abc import ABC, abstractmethod


class IPasswordService(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass
