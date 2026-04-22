from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import Account
from src.repos.alchemy import AccountRepo

from src.types import TokenPairDTO, SignInRequestDTO, SignUpRequestDTO

__all__ = ["AuthService"]


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = AccountRepo(session=session)

    async def sign_in(self, data: SignInRequestDTO) -> TokenPairDTO:
        pass

    async def sign_up(self, data: SignUpRequestDTO) -> Account:
        pass
