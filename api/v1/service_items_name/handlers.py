from fastapi import APIRouter
from starlette import status

from api.annotated_types import PageQuery, PageSizeQuery
from api.annotated_types.service_item_name import ItemNameID
from api.dependencies.services import ItemNameServiceDepends
from api.dependencies.services.auth import AuthenticateHeaderDepends
from src.types.pagination import Paginator
from src.types.service_item_name import ServiceItemNameBase

router = APIRouter(tags=["ServiceItemsName"], dependencies=[AuthenticateHeaderDepends])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=Paginator[ServiceItemNameBase]
)
async def get_service_car_list(
        service: ItemNameServiceDepends,
        page: PageQuery = 1,
        page_size: PageSizeQuery = 10,
) -> Paginator[ServiceItemNameBase]:
    return await service.list(page=page, page_size=page_size)


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ServiceItemNameBase
)
async def get_service_items_name(
        service: ItemNameServiceDepends,
        item_id: ItemNameID
) -> ServiceItemNameBase:
    return await service.get(item_id=item_id)


@router.post(
    path="/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceItemNameBase
)
async def create_service_items_name(
        service: ItemNameServiceDepends
) -> ServiceItemNameBase:
    return await service.create()


@router.patch(
    path="/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ServiceItemNameBase
)
async def update_service_items_name(
        item_id: ItemNameID,
        service: ItemNameServiceDepends
) -> ServiceItemNameBase:
    return await service.update(item_id=item_id)


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service_items_name(
        item_id: ItemNameID,
        service: ItemNameServiceDepends
) -> None:
    await service.delete(item_id=item_id)
