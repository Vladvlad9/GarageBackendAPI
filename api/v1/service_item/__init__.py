from fastapi import APIRouter
from .handlers import router

service_item = APIRouter(prefix="/service_item",)
service_item.include_router(router=router)