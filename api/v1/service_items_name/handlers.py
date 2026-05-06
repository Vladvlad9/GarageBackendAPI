from fastapi import APIRouter
from starlette import status

from api.dependencies.services.auth import AuthenticateHeaderDepends

router = APIRouter(tags=["ServiceItemsName"], dependencies=[AuthenticateHeaderDepends])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def get_service_car_list():
    pass


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
)
async def get_service_items_name():
    pass


@router.post(
    path="/{id}",
    status_code=status.HTTP_201_CREATED,
)
async def create_service_items_name():
    pass


@router.patch(
    path="/{id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_service_items_name():
    pass


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service_items_name():
    pass
