from src.service.auth.password_management import PasswordService
from src.service.auth.token_management import TokenService
from src.service.auth.blocklist_token_management import BlocklistTokenService

def get_password_service() -> PasswordService:
    """Provide PasswordService instance for dependency injection."""
    return PasswordService()

def get_token_service() -> TokenService:
    """Provide TokenService instance for dependency injection."""
    return TokenService()

def get_blocklist_token_service() -> BlocklistTokenService:
    """Provide TokenService instance for dependency injection."""
    return BlocklistTokenService()