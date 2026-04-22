from fastapi import APIRouter
from .auth import auth as auth_router
from .car import car as car_router

v1 = APIRouter(prefix="/v1")
v1.include_router(router=car_router)
v1.include_router(router=auth_router)
