from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import User
from src.exeptions import ObjectNotFoundError, IncorrectPasswordError, ObjectAlreadyExistError
from src.repos.alchemy import UserRepo

from src.types import TokenPairDTO, SignInRequestDTO, SignUpRequestDTO
from src.types.user import UserDetailResponseDTO
from src.utils.jwt import JWTManager

from src.utils.password import PasswordManager

__all__ = ["AuthService"]


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepo(session=session)

    async def sign_in(self, data: SignInRequestDTO) -> TokenPairDTO:
        user = await self.repo.get(filters=[User.email == str(data.email).lower()])
        if not user:
            raise ObjectNotFoundError(name="user")

        if not PasswordManager.check(plain_password=data.password, password_hash=user.password_hash):
            raise IncorrectPasswordError()

        return TokenPairDTO.model_validate(obj=await JWTManager.create_token_pair(user_id=user.id))

    async def sign_up(self, data: SignUpRequestDTO) -> UserDetailResponseDTO:
        user_data = data.model_dump(exclude={"password", "confirm"})
        user_data["name"] = str(data.name)
        user_data["email"] = str(data.email).lower()
        user_data["password_hash"] = PasswordManager.hash(plain_password=data.password)

        try:
            return await self.repo.insert(obj=user_data)
        except IntegrityError:
            raise ObjectAlreadyExistError(name="user")
