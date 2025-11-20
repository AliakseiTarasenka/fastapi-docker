import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from main import users_router
from src.infrastructure.dependencies.database import get_session
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.dependencies.services import get_password_service
from src.infrastructure.dependencies.services import get_token_service


@pytest.mark.asyncio
async def test_create_user_account(
    mock_user_repo, mock_token_service, mock_password_service, mock_session, mock_mail
):
    test_app = FastAPI()
    test_app.include_router(users_router)

    test_app.dependency_overrides[get_user_repository] = lambda: mock_user_repo
    test_app.dependency_overrides[get_token_service] = lambda: mock_token_service
    test_app.dependency_overrides[get_password_service] = lambda: mock_password_service
    test_app.dependency_overrides[get_session] = lambda: mock_session

    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://127.0.0.1",
        headers={"host": "127.0.0.1"},
    ) as client:
        response = await client.post(
            "/signup",
            json={
                "first_name": "Test",
                "last_name": "User",
                "username": "testuser",
                "email": "user@example.com",
                "password": "testpass123",
            },
        )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Account Created! Check email to verify your account"
    assert data["user"]["email"] == "user@example.com"
    assert data["user"]["username"] == "testuser"
