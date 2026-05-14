from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.exeptions import ObjectNotFoundError
from src.repos.alchemy import ServiceItemRepo
from src.types.service_item import ServiceItemBaseDTO
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

    async def create(self):
        pass

    async def update(self):
        pass

    async def delete(self):
        pass
