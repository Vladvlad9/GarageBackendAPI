from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.exception_handlers import ExceptionHandlerFactory
from api.exeption import (
    InternalServerException,
    ServiceResponseValidationException,
    ObjectNotFoundException,
    ObjectExistsException
)
from src.exeptions import ObjectNotFoundError, ObjectAlreadyExistError
from src.services.service_item_name import ItemNameService
from src.types.pagination import Paginator
from src.types.service_item_name import ServiceItemNameBase

item_name_exception_handler = ExceptionHandlerFactory(
    exc_mapping={
        ValidationError: ServiceResponseValidationException(name="item_name"),
        ObjectNotFoundError: ObjectNotFoundException(name="item_name"),
        ObjectAlreadyExistError: ObjectExistsException(name="item_name"),
    },
    default_exc=InternalServerException(name="item_name"),
)
__all__ = ["RESTItemNameService"]


class RESTItemNameService:
    def __init__(self, session: AsyncSession):
        self.item_name = ItemNameService(session=session)

    @item_name_exception_handler()
    async def get(self, item_id: UUID) -> ServiceItemNameBase:
        return await self.item_name.get(item_id=item_id)

    @item_name_exception_handler()
    async def create(self):
        pass

    @item_name_exception_handler()
    async def update(self, item_id: UUID):
        pass

    @item_name_exception_handler()
    async def delete(self, item_id: UUID):
        pass

    async def list(self, page: int, page_size: int) -> Paginator[ServiceItemNameBase]:
        return await self.item_name.list(page=page, page_size=page_size)
