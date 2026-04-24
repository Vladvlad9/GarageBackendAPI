from datetime import datetime
from typing import Annotated

from pydantic import Field

__all__ = ["CarBrandTypes", "ModelBrandTypes", "MileageTypes", "CarYearTypes"]

CarBrandTypes = Annotated[
    str,
    Field(
        ...,
        title="Название Бренда",
        description="Название Бренда",
        examples=["Audi"],
        min_length=2,
        max_length=100
    )
]

ModelBrandTypes = Annotated[
    str,
    Field(
        ...,
        title="Название модели",
        description="Название модели",
        examples=["A8", "RS7", "Q8"],
        min_length=1,
        max_length=100
    )
]

MileageTypes = Annotated[
    int,
    Field(
        ...,
        title="Текущий пробег",
        description="Текущий пробег",
        examples=[100],
        ge=1,
        le=999999
    )
]

CarYearTypes = Annotated[
    int,
    Field(
        ...,
        title="Год выпуска",
        description="Год выпуска",
        examples=[1900],
        ge=1900,
        le=datetime.now().year
    )
]