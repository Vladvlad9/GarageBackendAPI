from pathlib import Path
from typing import Annotated

from pydantic import Field

from settings._base import BaseSettingsConfig
from settings.server import ServerSettings
from settings.app import AppSettings
from settings.database import DataBaseSettings

__all__ = ["settings"]


class Settings(BaseSettingsConfig):
    BASE_DIR: Path = Path(__file__).parent.parent

    SERVER: Annotated[ServerSettings, Field(default_factory=ServerSettings)]
    APP: Annotated[AppSettings, Field(default_factory=AppSettings)]
    DATABASE: Annotated[DataBaseSettings, Field(default_factory=DataBaseSettings)]


settings = Settings()
