import redis.asyncio as aioredis

from config.settings import Config


class BlocklistTokenService:
    """
    Handles JWT token blocklist operations in Redis.
    """

    def __init__(self, redis_url: str = Config.REDIS_URL, expiry: int = Config.JTI_EXPIRY):
        self.redis_url = redis_url
        self.expiry = expiry
        self._redis = None

    async def connect(self):
        """Initialize Redis connection."""
        if self._redis is None:
            self._redis = aioredis.from_url(self.redis_url, decode_responses=True)

    async def disconnect(self):
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()
            self._redis = None

    async def add_to_blocklist(self, jti: str) -> None:
        """Add JTI to Redis blocklist with expiry."""
        await self.connect()
        await self._redis.set(name=jti, value="", ex=self.expiry)

    async def is_token_blocked(self, jti: str) -> bool:
        """Check if token JTI exists in blocklist."""
        await self.connect()
        result = await self._redis.get(jti)
        return result is not None
