import uuid

from src.types.base import ImmutableDTO

__all__ = ["ServiceItemNameBase"]


class ServiceItemNameBase(ImmutableDTO):
    id: uuid.UUID
    name: str
    icon: str
