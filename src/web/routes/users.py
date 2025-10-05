from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from db.database import get_session
from persistence.user_repository import UserRepository
from service.utils import create_access_token, verify_password
from web.schemas.users import UserCreateModel, UserLoginModel, UserModel

app = APIRouter()
user_repository = UserRepository()


@app.post(
    "/users/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email_exists = await user_repository.user_exists(user_data.email, session)

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user_data.email} already exists",
        )
    new_user = await user_repository.create_user(user_data, session)
    return new_user


@app.post("/users/login")
async def login_users(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    user = await user_repository.get_user_by_email(user_data.email, session)

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
