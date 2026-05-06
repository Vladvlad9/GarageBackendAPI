from datetime import datetime
from typing import Annotated, Literal, Any, List
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
    "CarBaseMutableDTO",
    "CarDetailResponseWithoutServiceItemsDTO",
]

from src.types.service_item import ServiceItemBaseDTO

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

    initials: str | None = None

    @model_validator(mode='after')
    def auto_initials(self) -> 'CarBaseMutableDTO':
        if self.brand and self.model:
            name = f"{self.brand} {self.model}"
            words = name.split()
            self.initials = ''.join(word[0] for word in words)[:2].upper()
        return self

    class Config:
        frozen = False


class CarBaseMutableDTO(CarBaseDTO):
    service_items: List[ServiceItemBaseDTO]

    initials: str | None = None

    @model_validator(mode='after')
    def auto_initials(self) -> 'CarBaseMutableDTO':
        if self.brand and self.model:
            name = f"{self.brand} {self.model}"
            words = name.split()
            self.initials = ''.join(word[0] for word in words)[:2].upper()
        return self

    class Config:
        frozen = False


class CarResponseIdDTO(ImmutableDTO):
    id: UUID


class CarFilterDTO(ImmutableDTO):
    q: Annotated[str | None, Field()] = None
    sort_by: Literal["id"] = Field(default="id")
    sort: Literal["asc", "desc"] = Field(default="asc")
    fuel_type: FuelTypeEnum | None = Field(default=None)
    transmission: TransmissionEnum | None = Field(default=None)


class CarDetailResponseDTO(CarBaseDTO):
    service_items: List[ServiceItemBaseDTO | None] = None

class CarDetailResponseWithoutServiceItemsDTO(CarBaseDTO):
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

    @model_validator(mode='before')
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

    @model_validator(mode='before')
    @classmethod
    def tess(cls, data: Any) -> Any:
        # data - это словарь или другой входной формат
        print("Полученные данные:", data)

        # # Доступ к полям как к ключам словаря
        # if isinstance(data, dict):
        #     print(data.get('brand'))  # используем .get() для безопасности
        #     print(data.get('model'))
        #     print(data.get('year'))
        # else:
        #     # Если это уже объект
        #     print(getattr(data, 'brand', None))
        #     print(getattr(data, 'model', None))
        #     print(getattr(data, 'year', None))

        return data


class CarDeleteRequestDTO(ImmutableDTO):
    is_archived: bool = True
    updated_at: datetime = now()
