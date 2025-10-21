from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from typing import Optional

from src.infrastructure.service.auth.blocklist_token_management import BlocklistTokenService
from src.infrastructure.service.auth.dependencies import get_token_service, get_blocklist_token_service
from src.infrastructure.service.auth.token_management import TokenService


class TokenBearer(HTTPBearer):

    def __init__(
            self,
            auto_error=True
    ) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(
            self,
            request: Request,
            blocklist_service: BlocklistTokenService = Depends(get_blocklist_token_service),
            token_service: TokenService = Depends(get_token_service)
    ) -> Optional[HTTPAuthorizationCredentials]:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = token_service.decode_token(token)

        if not token_data or "jti" not in token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token",
                },
            )

        if await blocklist_service.is_token_blocked(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get new token"
                }
            )

        if not self.token_valid(token_data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token",
                },
            )

        await self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token_data: dict) -> bool:
        return token_data is not None

    async def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):

    async def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):

    async def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )
