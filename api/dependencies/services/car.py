from typing import Annotated

from fastapi import Depends

from api.dependencies.database_session import DBSession
from api.services import RESTCarService

__all__ = ["CarServiceDepends"]


async def _car_service(session: DBSession) -> RESTCarService:
    return RESTCarService(session=session)


CarServiceDepends = Annotated[RESTCarService, Depends(dependency=_car_service)]
