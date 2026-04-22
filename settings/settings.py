from pathlib import Path
from typing import Annotated

from pydantic import Field

from settings._base import BaseSettingsConfig
from settings.jwt import JWTSettings
from settings.redis import RedisSettings
from settings.server import ServerSettings
from settings.app import AppSettings
from settings.database import DataBaseSettings

__all__ = ["settings"]


class Settings(BaseSettingsConfig):
    BASE_DIR: Path = Path(__file__).parent.parent

    SERVER: Annotated[ServerSettings, Field(default_factory=ServerSettings)]
    APP: Annotated[AppSettings, Field(default_factory=AppSettings)]
    DATABASE: Annotated[DataBaseSettings, Field(default_factory=DataBaseSettings)]
    JWT: Annotated[JWTSettings, Field(default_factory=JWTSettings)]
    REDIS: Annotated[RedisSettings, Field(default_factory=RedisSettings)]


settings = Settings()
