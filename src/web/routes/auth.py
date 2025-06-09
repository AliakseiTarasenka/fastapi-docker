from fastapi import (
    status,
    APIRouter,
    Depends,
)
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from service.utils import create_access_token, verify_password
from service.dependencies import RefreshTokenBearer
from datetime import datetime

app = APIRouter()

@app.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )