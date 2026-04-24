from sqlalchemy.ext.asyncio import AsyncSession

from src.database.alchemy.models import Car
from src.repos.alchemy.base import BaseRepo

__all__ = ["CarRepo"]


class CarRepo(BaseRepo[Car]):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=Car)
