from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.application.errors import UserAlreadyExists, InvalidCredentials
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.dependencies.services import (
    get_token_service,
    get_blocklist_token_service,
)
from src.infrastructure.repositories.users_repository import UserRepository
from src.infrastructure.service.auth.blocklist_token_management import BlocklistTokenService
from src.infrastructure.service.auth.token_bearer import AccessTokenBearer
from src.infrastructure.service.auth.token_management import TokenService
from src.presentation.web.schemas.users import UserCreateModel, UserLoginModel, UserModel

app = APIRouter()


@app.post("/users/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    user_repository: UserRepository = Depends(get_user_repository),
):
    user_exists = await user_repository.user_exists(user_data.email)

    if user_exists:
        raise UserAlreadyExists()
    new_user = await user_repository.create_user(user_data)
    return new_user


@app.post("/users/login")
async def login_users(
    user_data: UserLoginModel,
    user_repository: UserRepository = Depends(get_user_repository),
    token_service: TokenService = Depends(get_token_service),
):
    """Login a user. Verify the user's credentials. If valid - generate token and return the user."""
    user = await user_repository.get_user_by_email(user_data.email)

    if user is not None:
        if user_repository.password_service.verify_password(user_data.password, user.password_hash):
            access_token = token_service.create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )
            refresh_token = token_service.create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=7),
            )
            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )
    raise InvalidCredentials()


@app.post("/users/logout")
async def revoke_token(
    token_details: dict = Depends(AccessTokenBearer()),
    blocklist_token_service: BlocklistTokenService = Depends(get_blocklist_token_service),
):
    """Revoke a JWT token."""
    jti = token_details["jti"]
    await blocklist_token_service.add_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )
