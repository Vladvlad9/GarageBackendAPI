from fastapi import APIRouter
from starlette import status
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_409_CONFLICT
)

from api.annotated_types import ServiceItemID
from api.dependencies.services import ServiceItemDepends
from api.dependencies.services.auth import AuthenticateHeaderDepends

from src.types.exeptions import (
    ObjectNotFoundErrorDTO,
    HTTPExceptionErrorDTO,
    ToManyRequestsErrorDTO,
    ObjectAlreadyExistErrorDTO
)
from src.types.service_item import (
    ServiceItemBaseDTO,
    ServiceItemCreateDTO,
    ServiceItemCoreDTO
)

router = APIRouter(tags=["Service Item"], dependencies=[AuthenticateHeaderDepends])


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ServiceItemBaseDTO,
    responses={
        HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO},
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    },
)
async def get_service_item(
        service: ServiceItemDepends,
        service_id: ServiceItemID
) -> ServiceItemBaseDTO:
    return await service.get(service_id=service_id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceItemCoreDTO,
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
        HTTP_409_CONFLICT: {"model": ObjectAlreadyExistErrorDTO},
        HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
    }
)
async def create_service_item(
        service: ServiceItemDepends,
        data: ServiceItemCreateDTO
) -> ServiceItemCoreDTO:
    return await service.create(data=data)
