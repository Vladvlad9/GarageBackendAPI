from fastapi import APIRouter
from .handlers import router

auth = APIRouter(prefix="/auth")
auth.include_router(router)