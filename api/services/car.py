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
from src.services.car import CarService
from src.types.car import CarDetailResponseDTO, CarCreateDTO, CarUpdateRequestDTO, CarFilterDTO

from src.types.pagination import Paginator

car_exception_handler = ExceptionHandlerFactory(
    exc_mapping={
        ValidationError: ServiceResponseValidationException(name="car"),
        ObjectNotFoundError: ObjectNotFoundException(name="car"),
        ObjectAlreadyExistError: ObjectExistsException(name="car"),
    },
    default_exc=InternalServerException(name="car"),
)

__all__ = ["RESTCarService"]


class RESTCarService:
    def __init__(self, session: AsyncSession):
        self.car_service = CarService(session=session)

    async def car_list(self, page: int, page_size: int, filters: CarFilterDTO) -> Paginator[CarDetailResponseDTO]:
        return await self.car_service.car_list(page=page, page_size=page_size, filters=filters)

    @car_exception_handler()
    async def get(self, car_id: UUID, user_id: UUID | str) -> CarDetailResponseDTO:
        return await self.car_service.get(car_id=car_id, user_id=user_id)

    @car_exception_handler()
    async def create(self, data: CarCreateDTO, user_id: UUID | str) -> CarDetailResponseDTO:
        return await self.car_service.create(data=data, user_id=user_id)

    @car_exception_handler()
    async def update(self, car_id: UUID | str, user_id: UUID | str, data: CarUpdateRequestDTO) -> CarDetailResponseDTO:
        return await self.car_service.update(car_id=car_id, user_id=user_id, data=data)

    @car_exception_handler()
    async def delete(self, car_id: UUID | str, user_id: UUID | str) -> None:
        await self.car_service.soft_delete(car_id=car_id, user_id=user_id)
