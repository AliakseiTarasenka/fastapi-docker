from abc import ABC, abstractmethod
from datetime import timedelta


class ITokenService(ABC):
    """Abstract interface for token service"""

    @abstractmethod
    def create_access_token(
        self, user_data: dict, expiry: timedelta | None = None, refresh: bool = False
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decode a JWT token and handle invalid cases."""
        raise NotImplementedError()

    @abstractmethod
    def create_url_safe_token(self, data: dict):
        """Serialize a dict into a URLSafe token"""
        raise NotImplementedError()

    @abstractmethod
    def decode_url_safe_token(self, token: str):
        """Deserialize a URLSafe token to get data"""
        raise NotImplementedError()
