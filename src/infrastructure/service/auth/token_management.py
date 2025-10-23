import logging
import uuid
from datetime import datetime, timedelta, timezone

import jwt

from config.settings import Config


class TokenService:
    """Handles JWT token creation and decoding."""

    def __init__(self, secret: str = Config.JWT_SECRET, algorithm: str = Config.JWT_ALGORITHM):
        self.secret = secret
        self.algorithm = algorithm

    def create_access_token(
        self, user_data: dict, expiry: timedelta | None = None, refresh: bool = False
    ) -> str:
        """Create a signed JWT access or refresh token."""
        payload = {
            "user": user_data,
            "exp": datetime.now() + (expiry or timedelta(minutes=60)),
            "iat": datetime.now(timezone.utc),  # issued at
            "jti": str(uuid.uuid4()),  # unique token ID
            "refresh": refresh,
        }

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        """Decode a JWT token and handle invalid cases."""
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            logging.warning("Token expired.")
            return {}
        except jwt.PyJWTError as e:
            logging.exception(f"Invalid token: {e}")
            return {}
