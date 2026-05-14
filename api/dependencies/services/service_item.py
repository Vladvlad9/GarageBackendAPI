from typing import Annotated

from fastapi import Depends

from api.dependencies.database_session import DBSession
from api.services import RESTServiceItem

__all__ = ["ServiceItemDepends"]


async def _car_service(session: DBSession) -> RESTServiceItem:
    return RESTServiceItem(session=session)


ServiceItemDepends = Annotated[RESTServiceItem, Depends(dependency=_car_service)]
