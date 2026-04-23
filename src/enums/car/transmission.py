from enum import StrEnum, unique, auto

__all__ = ["TransmissionEnum"]


@unique
class TransmissionEnum(StrEnum):
    MANUAL = auto()
    AUTOMATIC = auto()
    CVT = auto()
    ROBOT = auto()
