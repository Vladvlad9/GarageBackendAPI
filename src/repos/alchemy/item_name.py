from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import ServiceItemName
from src.repos.alchemy.base import BaseRepo

__all__ = ["ItemNameRepo"]


class ItemNameRepo(BaseRepo[ServiceItemName]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ServiceItemName)
