from abc import ABC, abstractmethod
from datetime import timedelta

from itsdangerous import URLSafeTimedSerializer

from config.settings import Config


class ITokenService(ABC):
    def __init__(self, secret: str = Config.JWT_SECRET, algorithm: str = Config.JWT_ALGORITHM):
        self.secret = secret
        self.algorithm = algorithm
        self.serializer = URLSafeTimedSerializer(self.secret, salt="email-configuration")

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
