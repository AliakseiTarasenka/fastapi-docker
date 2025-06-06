from fastapi import (
    status,
    APIRouter,
    Depends,
)
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from service.users import UserService
from persistence.database import get_session
from web.schemas.users import UserCreateModel, UserLoginModel, UserModel
from src.service.utils import create_access_token, verify_password
from datetime import timedelta

app = APIRouter()
user_service = UserService()


@app.post(
    "/users/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email_exists = await user_service.user_exists(user_data.email, session)

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user_data.email} already exists",
        )
    new_user = await user_service.create_user(user_data, session)
    return new_user


@app.post("/users/login")
async def login_users(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    user = await user_service.get_user_by_email(user_data.email, session)

    if user is not None:
        if verify_password(user_data.password, user.password_hash):
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )
            refresh_token = create_access_token(
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
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password",
    )
