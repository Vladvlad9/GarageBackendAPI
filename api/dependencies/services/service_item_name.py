from typing import Annotated

from fastapi import Depends

from api.dependencies.database_session import DBSession

from api.services.item_name import RESTItemNameService

__all__ = ["ItemNameServiceDepends"]


async def _item_name_service(session: DBSession) -> RESTItemNameService:
    return RESTItemNameService(session=session)


ItemNameServiceDepends = Annotated[RESTItemNameService, Depends(dependency=_item_name_service)]
