import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from main import users_router
from src.infrastructure.dependencies.repositories import get_user_repository
from src.infrastructure.dependencies.services import get_password_service
from src.infrastructure.dependencies.services import get_token_service


@pytest.mark.asyncio
async def test_login_success(mock_user_repo, mock_token_service, mock_password_service):
    test_app = FastAPI()
    test_app.include_router(users_router)

    test_app.dependency_overrides[get_user_repository] = lambda: mock_user_repo
    test_app.dependency_overrides[get_token_service] = lambda: mock_token_service
    test_app.dependency_overrides[get_password_service] = lambda: mock_password_service

    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://127.0.0.1",
        headers={"host": "127.0.0.1"},
    ) as client:
        response = await client.post(
            "/login", json={"email": "user@example.com", "password": "secret"}
        )
    print(response)
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Login successful"
    assert data["user"]["email"] == "user@example.com"
    assert "access_token" in data
    assert "refresh_token" in data
