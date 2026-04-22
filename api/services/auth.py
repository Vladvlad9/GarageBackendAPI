from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.exception_handlers import ExceptionHandlerFactory
from api.exeption import (
    InternalServerException,
    ObjectExistsException,
    IncorrectPasswordException,
    ObjectNotFoundException,
    ServiceResponseValidationException
)
from src.database.alchemy.models import Account
from src.exeptions import ObjectNotFoundError, IncorrectPasswordError, ObjectAlreadyExistError
from src.services import AuthService
from src.types import TokenPairDTO, SignInRequestDTO, SignUpRequestDTO

__all__ = ["RESTAuthService"]

auth_exception_handler = ExceptionHandlerFactory(
    exc_mapping={
        ValidationError: ServiceResponseValidationException(name="auth"),
        ObjectNotFoundError: ObjectNotFoundException(name="account"),
        IncorrectPasswordError: IncorrectPasswordException,
        ObjectAlreadyExistError: ObjectExistsException(name="account"),
    },
    default_exc=InternalServerException(name="account"),
)


class RESTAuthService:
    def __init__(self, session: AsyncSession):
        self._auth_service = AuthService(session=session)

    async def sign_in(self, data: SignInRequestDTO) -> TokenPairDTO:
        return await self._auth_service.sign_in(data=data)

    async def sign_up(self, data: SignUpRequestDTO) -> Account:
        return await self._auth_service.sign_up(data=data)
