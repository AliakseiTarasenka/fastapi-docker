from abc import ABC, abstractmethod
from datetime import timedelta


class ITokenService(ABC):
    """Abstract interface for token service"""

    @abstractmethod
    def create_access_token(
        self, user_data: dict, expiry: timedelta | None = None, refresh: bool = False
    ) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decode a JWT token and handle invalid cases."""
        pass

    @abstractmethod
    def create_url_safe_token(self, data: dict):
        """Serialize a dict into a URLSafe token"""
        pass

    @abstractmethod
    def decode_url_safe_token(self, token: str):
        """Deserialize a URLSafe token to get data"""
        pass
