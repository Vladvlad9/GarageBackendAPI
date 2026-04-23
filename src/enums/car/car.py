from enum import StrEnum, unique, auto

__all__ = ["FuelTypeEnum"]


@unique
class FuelTypeEnum(StrEnum):
    PETROL = auto()
    DIESEL = auto()
    ELECTRIC = auto()
    GAS = auto()
    HYBRID = auto()
