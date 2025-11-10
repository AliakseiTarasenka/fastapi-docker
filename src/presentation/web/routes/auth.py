from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.application.errors import InvalidToken
from src.infrastructure.dependencies.authentication import get_current_user
from src.infrastructure.dependencies.authorization import get_role_checker
from src.infrastructure.dependencies.services import get_token_service
from src.infrastructure.service.auth.token_bearer import RefreshTokenBearer
from src.infrastructure.service.auth.token_management import TokenService
from src.presentation.web.schemas.users import UserBooksModel

app = APIRouter()
role_checker = get_role_checker(["user"])  # Define specific roles for users to be checked


@app.get("/refresh_token")
async def get_new_access_token(
        token_details: dict = Depends(RefreshTokenBearer()),
        token_service: TokenService = Depends(get_token_service),
):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = token_service.create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@app.get("/me", response_model=UserBooksModel)
async def get_user(user=Depends(get_current_user), _: bool = Depends(role_checker)):
    return user
