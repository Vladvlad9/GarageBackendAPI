from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, model_validator, PrivateAttr

from src.enums.car import FuelTypeEnum, TransmissionEnum
from src.types.annotated_types import CarBrandTypes, ModelBrandTypes, MileageTypes, CarYearTypes
from src.types.base import ImmutableDTO

__all__ = [
    "CarBaseDTO",
    "CarResponseIdDTO",
    "CarFilterDTO",
    "CarDetailResponseDTO",
    "CarCreateDTO",
    "CarUpdateRequestDTO",
    "CarDeleteRequestDTO",
]

from src.utils import now


class CarBaseDTO(ImmutableDTO):
    id: UUID
    name: str
    brand: CarBrandTypes
    model: ModelBrandTypes
    color: str
    year: CarYearTypes
    mileage: MileageTypes
    vin: str | None
    license_plate: str | None
    engine_volume: float | None
    fuel_type: FuelTypeEnum | None
    transmission: TransmissionEnum | None
    notes: str | None
    is_archived: bool

    created_at: datetime
    updated_at: datetime | None


class CarResponseIdDTO(ImmutableDTO):
    id: UUID


class CarFilterDTO(ImmutableDTO):
    q: Annotated[str | None, Field()] = None
    sort_by: Literal["id"] = Field(default="id")
    sort: Literal["asc", "desc"] = Field(default="asc")
    fuel_type: FuelTypeEnum | None = Field(default=None)
    transmission: TransmissionEnum | None = Field(default=None)


class CarDetailResponseDTO(CarBaseDTO):
    pass


class CarUpdateRequestDTO(ImmutableDTO):
    _name: str | None = PrivateAttr(default=None)
    brand: CarBrandTypes | None = None
    model: ModelBrandTypes | None = None
    color: str | None = None
    year: CarYearTypes | None = None
    mileage: MileageTypes | None = None
    vin: str | None = None
    license_plate: str | None = None
    engine_volume: float | None = None
    fuel_type: FuelTypeEnum | None = None
    transmission: TransmissionEnum | None = None
    notes: str | None = None
    is_archived: bool | None = None

    @model_validator(mode='after')
    def auto_generate_name(self) -> 'CarUpdateRequestDTO':
        if self._name is not None:
            return self

        brand_value = self.brand if self.brand else None
        model_value = self.model if self.model else None

        if brand_value and model_value:
            self._name = f"{brand_value} {model_value}"
        return self


class CarCreateDTO(ImmutableDTO):
    brand: CarBrandTypes
    model: ModelBrandTypes
    year: CarYearTypes
    mileage: MileageTypes


class CarDeleteRequestDTO(ImmutableDTO):
    is_archived: bool = True
    updated_at: datetime = now()
