from src.infrastructure.database.database import get_session
from src.infrastructure.repositories.users_repository import UserRepository
from src.infrastructure.service.auth.password_management import PasswordService


def get_user_repository() -> UserRepository:
    password_service = PasswordService()
    session = get_session()
    return UserRepository(session=session, password_service=password_service)
