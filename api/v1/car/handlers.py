from fastapi import APIRouter, Depends
from starlette import status
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_409_CONFLICT
)

from api.annotated_types import CarID, PageQuery, PageSizeQuery
from api.dependencies.services import CarServiceDepends
from api.dependencies.services.auth import TokenPayloadDepends, AuthenticateHeaderDepends
from src.types.car import (
    CarDetailResponseDTO,
    CarCreateDTO,
    CarUpdateRequestDTO,
    CarFilterDTO
)
from src.types.exeptions import (
    ToManyRequestsErrorDTO,
    HTTPExceptionErrorDTO,
    ObjectNotFoundErrorDTO,
    ObjectAlreadyExistErrorDTO
)
from src.types.pagination import Paginator

router = APIRouter(tags=["Car"], dependencies=[AuthenticateHeaderDepends])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=Paginator[CarDetailResponseDTO],
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
)
async def car_list(
        service: CarServiceDepends,
        page: PageQuery = 1,
        page_size: PageSizeQuery = 10,
        filters: CarFilterDTO = Depends()
) -> Paginator[CarDetailResponseDTO]:
    return await service.car_list(page=page, page_size=page_size, filters=filters)


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    response_model=CarDetailResponseDTO,
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
)
async def get(
        car_id: CarID,
        service: CarServiceDepends,
        payload: TokenPayloadDepends
) -> CarDetailResponseDTO:
    return await service.get(car_id=car_id, user_id=payload.get("sub"))


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CarDetailResponseDTO,
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_409_CONFLICT: {"model": ObjectAlreadyExistErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    }
)
async def create(
        data: CarCreateDTO,
        service: CarServiceDepends,
        payload: TokenPayloadDepends
) -> CarDetailResponseDTO:
    return await service.create(data=data, user_id=payload.get("sub"))


@router.patch(
    path="/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CarDetailResponseDTO,
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
)
async def update(
        car_id: CarID,
        service: CarServiceDepends,
        payload: TokenPayloadDepends,
        data: CarUpdateRequestDTO
) -> CarDetailResponseDTO:
    return await service.update(car_id=car_id, user_id=payload.get("sub"), data=data)


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
)
async def delete(car_id: CarID, service: CarServiceDepends, payload: TokenPayloadDepends) -> None:
    await service.delete(car_id=car_id, user_id=payload.get("sub"))
