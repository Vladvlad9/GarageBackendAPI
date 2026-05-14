from fastapi import APIRouter
from starlette import status

from api.annotated_types import ServiceItemID
from api.dependencies.services import ServiceItemDepends
from api.dependencies.services.auth import AuthenticateHeaderDepends

router = APIRouter(tags=["Service Item"], dependencies=[AuthenticateHeaderDepends])


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
)
async def get_service_item(
        service: ServiceItemDepends,
        service_id: ServiceItemID
):
    pass
