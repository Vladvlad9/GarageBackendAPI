from math import ceil
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import Car
from src.exeptions import ObjectNotFoundError, InternalServerError
from src.repos.alchemy import CarRepo

from src.types.car import CarDetailResponseDTO, CarCreateDTO, CarFilterDTO, CarDeleteRequestDTO
from src.types.pagination import Paginator, Pagination

__all__ = ["CarService"]


class CarService:
    def __init__(self, session: AsyncSession):
        self._repo = CarRepo(session=session)

    async def get_actual_car(self, car_id: UUID | str, user_id: UUID | str) -> Car:
        filters = [Car.id == car_id, Car.is_archived == False, Car.user_id == user_id]
        car = await self._repo.get(filters=filters)
        if not car:
            raise ObjectNotFoundError(name="Update_Car")
        return car

    async def get(self, car_id: UUID, user_id: UUID | str) -> CarDetailResponseDTO:
        car = await self.get_actual_car(car_id=car_id, user_id=user_id)
        return CarDetailResponseDTO.model_validate(obj=car)

    async def create(self, data: CarCreateDTO, user_id: UUID | str) -> CarDetailResponseDTO:
        car_data = data.model_dump()
        car_data["user_id"] = user_id
        car_data["name"] = f"{data.brand} {data.model}"
        try:
            car = await self._repo.insert(obj=car_data)
            return CarDetailResponseDTO.model_validate(obj=car)
        except IntegrityError:
            raise InternalServerError(name="Create_Car")

    async def update(self, car_id: UUID, user_id: UUID | str, data) -> CarDetailResponseDTO:
        await self.get_actual_car(car_id=car_id, user_id=user_id)

        filters = [Car.id == car_id, Car.is_archived == False, Car.user_id == user_id]
        obj = data.model_dump(exclude_unset=True, exclude_none=True)

        if hasattr(data, '_name') and data._name is not None:
            obj['name'] = data._name

        car = await self._repo.update(obj=obj, filters=filters)

        if not car:
            raise ObjectNotFoundError(name="Update_Car")

        return CarDetailResponseDTO.model_validate(obj=car)

    async def delete(self, car_id: UUID, user_id: UUID | str) -> None:
        car = await self.get_actual_car(car_id=car_id, user_id=user_id)
        # _car = await self._repo.delete(filters=filters)

    async def car_list(self, page: int, page_size: int, filters: CarFilterDTO) -> Paginator[CarDetailResponseDTO]:
        count = await self._repo.count()
        filter_conditions = []

        if filters.fuel_type is not None:
            filter_conditions.append(Car.fuel_type == filters.fuel_type)

        if filters.transmission is not None:
            filter_conditions.append(Car.transmission == filters.transmission)

        cars = await self._repo.list_data(
            page=page,
            page_size=page_size,
            filters=[*filter_conditions] if filter_conditions else None,
        )

        return Paginator(
            results=[CarDetailResponseDTO.model_validate(obj=car) for car in cars],
            pagination=Pagination(
                page_size=page_size,
                page=page,
                page_count=ceil(count / page_size) if count > 0 else 1,
            ),
        )

    async def soft_delete(self, car_id: UUID, user_id: UUID | str) -> None:
        await self.get_actual_car(car_id=car_id, user_id=user_id)
        filters = [Car.id == car_id, Car.is_archived == False, Car.user_id == user_id]

        obj = CarDeleteRequestDTO()
        await self._repo.soft_delete(obj=obj.model_dump(), filters=filters)
