from fastapi import APIRouter
from starlette import status
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_409_CONFLICT
)
from api.annotated_types import PageQuery, PageSizeQuery
from api.annotated_types.service_item_name import ItemNameID
from api.dependencies.services import ItemNameServiceDepends
from api.dependencies.services.auth import AuthenticateHeaderDepends
from src.types.exeptions import (
    ObjectNotFoundErrorDTO,
    HTTPExceptionErrorDTO,
    ToManyRequestsErrorDTO,
    ObjectAlreadyExistErrorDTO
)
from src.types.pagination import Paginator
from src.types.service_item_name import ServiceItemNameBase, ItemNameCreateDTO, ItemNameUpdateDTO

router = APIRouter(tags=["ServiceItemsName"], dependencies=[AuthenticateHeaderDepends])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=Paginator[ServiceItemNameBase],
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
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
    response_model=ServiceItemNameBase,
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
)
async def get_service_items_name(
        service: ItemNameServiceDepends,
        item_id: ItemNameID
) -> ServiceItemNameBase:
    return await service.get(item_id=item_id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceItemNameBase,
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_409_CONFLICT: {"model": ObjectAlreadyExistErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    }
)
async def create_service_items_name(
        data: ItemNameCreateDTO,
        service: ItemNameServiceDepends
) -> ServiceItemNameBase:
    return await service.create(data=data)


@router.patch(
    path="/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ServiceItemNameBase,
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
)
async def update_service_items_name(
        item_id: ItemNameID,
        data: ItemNameUpdateDTO,
        service: ItemNameServiceDepends
) -> ServiceItemNameBase:
    return await service.update(item_id=item_id, data=data)


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
)
async def delete_service_items_name(
        item_id: ItemNameID,
        service: ItemNameServiceDepends
) -> None:
    await service.delete(item_id=item_id)
