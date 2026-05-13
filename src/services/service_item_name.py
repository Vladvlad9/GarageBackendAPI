from math import ceil
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import ServiceItemName
from src.exeptions import ObjectNotFoundError, InternalServerError, ObjectAlreadyExistError
from src.repos.alchemy import ItemNameRepo
from src.types.pagination import Paginator, Pagination

from src.types.service_item_name import ServiceItemNameBase, ItemNameCreateDTO, ItemNameUpdateDTO

__all__ = ['ItemNameService']


class ItemNameService:
    def __init__(self, session: AsyncSession):
        self._repo = ItemNameRepo(session=session)

    async def get_actual_item_name(self, name: str = None, item_id: UUID = None) -> ServiceItemNameBase:
        filters = []

        if name:
            filters = [ServiceItemName.name == name]
        if item_id:
            filters = [ServiceItemName.id == item_id]

        item_name = await self._repo.get(filters=filters)
        if not item_name:
            raise ObjectNotFoundError(name="ItemName")
        return ServiceItemNameBase.model_validate(obj=item_name)

    async def get(self, item_id: UUID) -> ServiceItemNameBase:
        filters = [ServiceItemName.id == item_id]
        item_name = await self._repo.get(filters=filters)
        if not item_name:
            raise ObjectNotFoundError(name="ItemName")
        return ServiceItemNameBase.model_validate(item_name)

    async def create(self, data: ItemNameCreateDTO) -> ServiceItemNameBase:
        item_data = data.model_dump()
        if await self.get_actual_item_name(name=data.name):
            raise ObjectAlreadyExistError(name="Create_ItemName")

        try:
            item_name = await self._repo.insert(obj=item_data)
            return ServiceItemNameBase.model_validate(obj=item_name)
        except IntegrityError:
            raise InternalServerError(name="Create_ItemName")

    async def update(self, item_id: UUID, data: ItemNameUpdateDTO):
        await self.get_actual_item_name(item_id=item_id)

        obj = data.model_dump(exclude_unset=True, exclude_none=True)
        filters = [ServiceItemName.id == item_id]
        try:
            item_name = await self._repo.update(obj=obj, filters=filters)
            return ServiceItemNameBase.model_validate(obj=item_name)
        except IntegrityError:
            raise InternalServerError(name="Update_ItemName")

    async def delete(self, item_id: UUID) -> None:
        await self.get_actual_item_name(item_id=item_id)
        filters = [ServiceItemName.id == item_id]
        await self._repo.delete(filters=filters)

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
