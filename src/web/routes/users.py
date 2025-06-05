from fastapi import (
    status,
    APIRouter,
    Depends,
)
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.service.users import UserService
from src.persistence.database import get_session
from src.web.schemas.users import UserCreateModel
from src.models.users import User

app = APIRouter()
user_service = UserService()


@app.post("/users/signup", response_model=User, status_code=status.HTTP_201_CREATED)
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
