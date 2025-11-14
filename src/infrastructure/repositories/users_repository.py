from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.users import User
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.services.password_interface import IPasswordService
from src.presentation.web.schemas.users import UserCreateModel


class UserRepository(IUserRepository):

    def __init__(self, session: AsyncSession, password_service: IPasswordService):
        self.session = session
        self.password_service = password_service

    async def get_user_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        user = result.first()

        return user

    async def user_exists(self, email: str) -> bool:
        user = await self.get_user_by_email(email)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel) -> User:
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = self.password_service.hash_password(user_data_dict["password"])
        self.session.add(new_user)

        await self.session.commit()

        return new_user

    async def delete_user(self, email: str) -> bool:
        user = await self.get_user_by_email(email)

        if user is not None:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False
