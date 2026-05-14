from sqlalchemy.ext.asyncio import AsyncSession

from src.repos.alchemy import ServiceItemRepo

__all__ = ["ServiceItem"]


class ServiceItem:
    def __init__(self, session: AsyncSession):
        self._repo = ServiceItemRepo(session=session)

    async def get(self):
        pass

    async def create(self):
        pass

    async def update(self):
        pass

    async def delete(self):
        pass
