from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import ServiceItem
from src.repos.alchemy.base import BaseRepo

__all__ = ["ServiceItemRepo"]


class ServiceItemRepo(BaseRepo[ServiceItem]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=ServiceItem)
