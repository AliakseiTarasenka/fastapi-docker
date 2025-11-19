from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.models.users import User
from src.domain.repositories.user_repository_interface import IUserRepository
from src.domain.services.password_interface import IPasswordService
from src.presentation.web.schemas.users import UserCreateModel


class UserRepository(IUserRepository):

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()

        return user

    async def user_exists(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(
        self, user_data: UserCreateModel, session: AsyncSession, password_service: IPasswordService
    ) -> User:
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = password_service.hash_password(user_data_dict["password"])
        session.add(new_user)

        await session.commit()

        return new_user

    async def delete_user(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)

        if user is not None:
            await session.delete(user)
            await session.commit()
            return True
        return False

    async def update_user(self, user: User, user_data: dict, session: AsyncSession) -> User:
        for key, value in user_data.items():
            setattr(user, key, value)

        await session.commit()

        return user
