from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import Account
from src.exeptions import ObjectNotFoundError, IncorrectPasswordError, ObjectAlreadyExistError
from src.repos.alchemy import AccountRepo

from src.types import TokenPairDTO, SignInRequestDTO, SignUpRequestDTO
from src.utils.jwt import JWTManager

from src.utils.password import PasswordManager

__all__ = ["AuthService"]


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = AccountRepo(session=session)

    async def sign_in(self, data: SignInRequestDTO) -> TokenPairDTO:
        account = await self.repo.get(filters=[Account.email == str(data.email).lower()])
        if not account:
            raise ObjectNotFoundError(name="account")

        if not PasswordManager.check(plain_password=data.password, password_hash=account.password_hash):
            raise IncorrectPasswordError()

        return TokenPairDTO.model_validate(obj=await JWTManager.create_token_pair(user_id=account.id))

    async def sign_up(self, data: SignUpRequestDTO) -> Account:
        account_data = data.model_dump(exclude={"password"})
        account_data["email"] = str(data.email).lower()
        account_data["password_hash"] = PasswordManager.hash(plain_password=data.password)

        try:
            return await self.repo.insert(obj=account_data)
        except IntegrityError:
            raise ObjectAlreadyExistError(name="account")
