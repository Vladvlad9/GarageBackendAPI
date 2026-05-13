import uuid

from src.types.base import ImmutableDTO

__all__ = ["ServiceItemNameBase", "ItemNameCreateDTO", "ItemNameUpdateDTO"]


class ServiceItemNameBase(ImmutableDTO):
    id: uuid.UUID
    name: str
    icon: str


class ItemNameCreateDTO(ImmutableDTO):
    name: str
    icon: str


class ItemNameUpdateDTO(ImmutableDTO):
    name: str | None = None
    icon: str | None = None
