from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.exeptions import ObjectNotFoundError, InternalServerError
from src.repos.alchemy import ServiceItemRepo
from src.types.service_item import ServiceItemBaseDTO, ServiceItemCreateDTO, ServiceItemCoreDTO
from src.database.alchemy.models import ServiceItem as ServiceItemModel

__all__ = ["ServiceItem"]


class ServiceItem:
    def __init__(self, session: AsyncSession):
        self._repo = ServiceItemRepo(session=session)

    async def get(self, service_id: UUID) -> ServiceItemBaseDTO:
        filters = [ServiceItemModel.id == service_id, ServiceItemModel.is_active == True]
        options = [joinedload(ServiceItemModel.service_item_name)]
        service = await self._repo.get(filters=filters, options=options)

        if not service:
            raise ObjectNotFoundError(name="Car")

        return ServiceItemBaseDTO.model_validate(obj=service)

    async def create(self, data: ServiceItemCreateDTO) -> ServiceItemCoreDTO:
        service_data = data.model_dump()
        service_data["interval_km"] = 1
        service_data["interval_days"] = 1

        try:
            service = await self._repo.insert(obj=service_data)
            return ServiceItemCoreDTO.model_validate(obj=service)
        except IntegrityError:
            raise InternalServerError(name="Create_ServiceItem")

    async def update(self):
        pass

    async def delete(self):
        pass
