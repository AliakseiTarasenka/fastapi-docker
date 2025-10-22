from passlib.context import CryptContext


class PasswordService:
    """Handles password hashing and verification."""

    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Generate bcrypt hash for a password."""
        return self._context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify that a plain password matches the hashed one."""
        return self._context.verify(password, hashed_password)
