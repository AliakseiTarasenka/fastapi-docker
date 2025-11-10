from src.domain.services.authentication_interface import AuthenticationService


class Authentication:

    def __init__(self, auth_service: AuthenticationService):
        self.auth_service = auth_service

    async def execute(self, email: str, password: str):
        return await self.auth_service.authenticate_user(email, password)
