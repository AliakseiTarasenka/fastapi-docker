from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.application.errors import UserNotFound, InvalidToken
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.services.token_interface import ITokenService
from src.infrastructure.dependencies.authentication import get_current_user
from src.infrastructure.dependencies.authorization import get_role_checker
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.dependencies.services import (
    get_token_service,
)
from src.infrastructure.service.auth.token_bearer import RefreshTokenBearer
from src.presentation.web.schemas.users import UserBooksModel

auth_router = APIRouter()
role_checker = get_role_checker(["user"])  # Define specific roles for users to be checked


@auth_router.get("/refresh_token")
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()),
    token_service: ITokenService = Depends(get_token_service),
):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = token_service.create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/me", response_model=UserBooksModel)
async def get_user(user=Depends(get_current_user), _: bool = Depends(role_checker)):
    return user


@auth_router.get("/verify/{token}")
async def verify_user_account(
    token: str,
    token_service: ITokenService = Depends(get_token_service),
    user_repository: IUserRepository = Depends(get_user_repository),
):
    token_data = token_service.decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_repository.get_user_by_email(user_email)

        if not user:
            raise UserNotFound()

        await user_repository.update_user(user, {"is_verified": True})

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
