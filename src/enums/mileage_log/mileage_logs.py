from enum import StrEnum, unique, auto

__all__ = ["MileageLogsEnum"]


@unique
class MileageLogsEnum(StrEnum):
    MANUAL = auto()
    OBD = auto()
    SERVICE = auto()
