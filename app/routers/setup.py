from fastapi import FastAPI
from api import api


def include_routers(app: FastAPI) -> None:
    app.include_router(router=api)
