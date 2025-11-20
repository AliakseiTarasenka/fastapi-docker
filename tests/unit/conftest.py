import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.models.users import User
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.services.password_interface import IPasswordService
from src.domain.services.token_interface import ITokenService


@pytest.fixture
def test_user() -> User:
    return User(
        uid=uuid.uuid4(),
        username="testuser",
        first_name="Test",
        last_name="User",
        email="user@example.com",
        role="user",
        is_verified=True,
        password_hash="hashed_password",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def mock_user_repo(test_user):
    """Mocked UserRepository implementing IUserRepository"""
    mock_repo = MagicMock(spec=IUserRepository)

    # Mock user repository methods
    mock_repo.get_user_by_email = AsyncMock(return_value=test_user)
    mock_repo.user_exists = AsyncMock(return_value=False)
    mock_repo.create_user = AsyncMock(return_value=test_user)
    mock_repo.delete_user = AsyncMock(return_value=True)
    mock_repo.update_user = AsyncMock(return_value=test_user)

    return mock_repo


@pytest.fixture
def mock_token_service():
    token_service = MagicMock(spec=ITokenService)
    token_service.create_access_token.return_value = "mock_access_token"
    return token_service


@pytest.fixture
def mock_password_service():
    password_service = MagicMock(spec=IPasswordService)
    password_service.verify_password.return_value = True
    password_service.hash_password.return_value = "hashed_password"
    return password_service


@pytest.fixture
def mock_mail(monkeypatch):
    async def fake_send_message(message):
        return True

    monkeypatch.setattr(
        "src.infrastructure.mail.mail.send_message",
        fake_send_message,
    )


@pytest.fixture
def mock_session():
    class DummySession:
        async def commit(self):
            pass

        async def rollback(self):
            pass

        async def close(self):
            pass

    return DummySession()
