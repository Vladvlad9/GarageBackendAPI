from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import ServiceItemName
from src.exeptions import ObjectNotFoundError
from src.repos.alchemy import ItemNameRepo
from src.types.pagination import Paginator

__all__ = ['ItemNameService']

from src.types.service_item_name import ServiceItemNameBase


class ItemNameService:
    def __init__(self, session: AsyncSession):
        self._repo = ItemNameRepo(session=session)

    async def get(self, item_id: UUID) -> ServiceItemNameBase:
        filters = [ServiceItemName.id == item_id]
        item_name = await self._repo.get(filters=filters)
        if not item_name:
            raise ObjectNotFoundError(name="ItemName")
        return ServiceItemNameBase.model_validate(item_name)

    async def create(self):
        pass

    async def update(self, item_id: UUID):
        pass

    async def delete(self, item_id: UUID):
        pass

    async def list(self) -> Paginator[...]:
        pass
