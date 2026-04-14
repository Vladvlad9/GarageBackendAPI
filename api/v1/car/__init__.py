from fastapi import APIRouter
from .handlers import router

car = APIRouter(prefix="/car")
car.include_router(router)
