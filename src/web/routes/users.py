from fastapi import (
    status,
    APIRouter,
    Depends,
)
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.service.users import UserService

app = APIRouter()
user_service = UserService()
