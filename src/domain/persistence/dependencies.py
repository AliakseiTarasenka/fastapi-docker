from src.domain.persistence.user_repository import UserRepository
from src.infrastructure.service.auth.password_management import PasswordService


def get_user_repository() -> UserRepository:
    password_service = PasswordService()
    return UserRepository(password_service=password_service)
