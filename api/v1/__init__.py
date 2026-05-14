from fastapi import APIRouter
from .auth import auth as auth_router
from .car import car as car_router
from .service_items_name import service_items_name as service_items_name_router
from .service_item import service_item as service_item_router

v1 = APIRouter(prefix="/v1")
v1.include_router(router=car_router)
v1.include_router(router=auth_router)
v1.include_router(router=service_items_name_router)
v1.include_router(router=service_item_router)
