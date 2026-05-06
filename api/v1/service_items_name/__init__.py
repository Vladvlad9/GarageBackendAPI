from fastapi import APIRouter
from .handlers import router

service_items_name = APIRouter(
    prefix='/service_item_name',
)
service_items_name.include_router(router=router)