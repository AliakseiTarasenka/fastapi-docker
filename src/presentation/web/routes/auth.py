from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from src.infrastructure.service.authentication import RefreshTokenBearer
from src.infrastructure.service.authorization import get_current_user, RoleChecker
from src.infrastructure.service.utils import create_access_token
from src.presentation.web.schemas.users import UserBooksModel

app = APIRouter()
role_checker = RoleChecker(["user"])  # Define specific roles for users to be checked


@app.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired token"
    )


@app.get("/me", response_model=UserBooksModel)
async def get_current_user(user=Depends(get_current_user), _: bool = Depends(role_checker)):
    return user
