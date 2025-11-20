from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from config.settings import Config
from src.application.errors import UserAlreadyExists, InvalidCredentials
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.services.password_interface import IPasswordService
from src.domain.services.token_interface import ITokenService
from src.infrastructure.dependencies.database import get_session
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.dependencies.services import (
    get_token_service,
    get_blocklist_token_service,
    get_password_service,
)
from src.infrastructure.mail import mail, create_message
from src.infrastructure.service.auth.blocklist_token_management import BlocklistTokenService
from src.infrastructure.service.auth.token_bearer import AccessTokenBearer
from src.presentation.web.schemas.users import (
    UserCreateModel,
    UserLoginModel,
    UserModel,
    UserSignupResponse,
)

app = APIRouter()


@app.post("/signup", response_model=UserSignupResponse, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    user_repository: IUserRepository = Depends(get_user_repository),
    token_service: ITokenService = Depends(get_token_service),
    password_service: IPasswordService = Depends(get_password_service),
    session: AsyncSession = Depends(get_session),
):
    user_exists = await user_repository.user_exists(user_data.email, session=session)

    if user_exists:
        raise UserAlreadyExists()
    token = token_service.create_url_safe_token({"email": user_data.email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html_message = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your email</p>
        """
    message = create_message(
        recipients=[user_data.email], subject="Verify your email", body=html_message
    )

    await mail.send_message(message)

    new_user = await user_repository.create_user(
        user_data, session=session, password_service=password_service
    )
    user = UserModel(
        uid=new_user.uid,
        username=new_user.username,
        email=new_user.email,
        password_hash=new_user.password_hash,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        is_verified=new_user.is_verified,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
    )

    return {
        "message": "Account Created! Check email to verify your account",
        "user": user,
    }


@app.post("/login")
async def login_users(
    user_data: UserLoginModel,
    user_repository: IUserRepository = Depends(get_user_repository),
    token_service: ITokenService = Depends(get_token_service),
    password_service: IPasswordService = Depends(get_password_service),
    session: AsyncSession = Depends(get_session),
):
    """Login a user. Verify the user's credentials. If valid - generate token and return the user."""
    user = await user_repository.get_user_by_email(user_data.email, session=session)
    if not user:
        raise InvalidCredentials()

    if user is not None:
        if password_service.verify_password(user_data.password, user.password_hash):
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


@app.post("/logout")
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
