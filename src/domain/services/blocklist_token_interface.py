from abc import ABC, abstractmethod


class IBlocklistTokenService(ABC):
    """
    Handles JWT token blocklist operations in Redis.
    """

    @abstractmethod
    async def connect(self):
        """Initialize Redis connection."""

    @abstractmethod
    async def disconnect(self):
        """Close Redis connection."""

    @abstractmethod
    async def add_to_blocklist(self, jti: str) -> None:
        """Add JTI to Redis blocklist with expiry."""

    @abstractmethod
    async def is_token_blocked(self, jti: str) -> bool:
        """Check if token JTI exists in blocklist."""
