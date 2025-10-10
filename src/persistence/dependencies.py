from src.service.auth.password_management import PasswordService
from src.persistence.user_repository import UserRepository

def get_user_repository() -> UserRepository:
    password_service = PasswordService()
    return UserRepository(password_service=password_service)