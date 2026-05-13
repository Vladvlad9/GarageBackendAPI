from math import ceil
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import ServiceItemName
from src.exeptions import ObjectNotFoundError
from src.repos.alchemy import ItemNameRepo
from src.types.pagination import Paginator, Pagination

from src.types.service_item_name import ServiceItemNameBase

__all__ = ['ItemNameService']


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

    async def list(self, page: int, page_size: int) -> Paginator[ServiceItemNameBase]:
        count = await self._repo.count()
        items_name = await self._repo.list_data(page=page, page_size=page_size)

        return Paginator(
            results=[ServiceItemNameBase.model_validate(obj=item_name) for item_name in items_name],
            pagination=Pagination(
                page=page,
                page_size=page_size,
                page_count=ceil(count / page_size) if count > 0 else 1
            )
        )
