from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from api.exception_handlers import ExceptionHandlerFactory
from api.exeption import (
    ServiceResponseValidationException,
    ObjectNotFoundException,
    ObjectExistsException,
    InternalServerException
)
from src.exeptions import ObjectNotFoundError, ObjectAlreadyExistError
from src.services import ServiceItem

__all__ = ["RESTServiceItem"]

from src.types.service_item import ServiceItemBaseDTO

service_item_exception_handler = ExceptionHandlerFactory(
    exc_mapping={
        ValidationError: ServiceResponseValidationException(name="service_item"),
        ObjectNotFoundError: ObjectNotFoundException(name="service_item"),
        ObjectAlreadyExistError: ObjectExistsException(name="service_item"),
    },
    default_exc=InternalServerException(name="service_item"),
)


class RESTServiceItem:
    def __init__(self, session: AsyncSession):
        self.car_service = ServiceItem(session=session)

    @service_item_exception_handler()
    async def get(self, service_id: UUID) -> ServiceItemBaseDTO:
        return await self.car_service.get(service_id=service_id)

    @service_item_exception_handler()
    async def create(self):
        return await self.car_service.create()

    @service_item_exception_handler()
    async def update(self):
        return await self.car_service.update()

    @service_item_exception_handler()
    async def delete(self) -> None:
        await self.car_service.delete()
