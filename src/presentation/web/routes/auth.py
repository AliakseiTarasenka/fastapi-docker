from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from config.settings import Config
from src.application.errors import UserNotFound, InvalidToken, PasswordsDoNotMatch
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.services.token_interface import ITokenService
from src.infrastructure.dependencies.authentication import get_current_user
from src.infrastructure.dependencies.authorization import get_role_checker
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.dependencies.services import (
    get_token_service,
)
from src.infrastructure.mail import mail, create_message
from src.infrastructure.service.auth.token_bearer import RefreshTokenBearer
from src.presentation.web.schemas.passwords import (
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
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


@auth_router.post("/password-reset-request")
async def password_reset_request(
    email_data: PasswordResetRequestModel, token_service: ITokenService = Depends(get_token_service)
):
    email = email_data.email

    token = token_service.create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
    """
    subject = "Reset Your Password"

    message = create_message(recipients=[email], subject=subject, body=html_message)
    await mail.send_message(message)
    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    user_repository: IUserRepository = Depends(get_user_repository),
    token_service: ITokenService = Depends(get_token_service),
):
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password

    if new_password != confirm_password:
        raise PasswordsDoNotMatch()

    token_data = token_service.decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_repository.get_user_by_email(user_email)

        if not user:
            raise UserNotFound()

        passwd_hash = user_repository.password_service.hash_password(new_password)
        await user_repository.update_user(user, {"password_hash": passwd_hash})

        return JSONResponse(
            content={"message": "Password reset Successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
