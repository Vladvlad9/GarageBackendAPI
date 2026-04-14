from fastapi import APIRouter

from .car import car as car_router

v1 = APIRouter(prefix="/v1")
v1.include_router(router=car_router)