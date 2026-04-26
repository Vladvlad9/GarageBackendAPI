from datetime import date
from uuid import UUID

from src.types.base import ImmutableDTO

__all__ = ["ServiceItemResponseDTO", "ServiceItemBaseDTO"]


class ServiceItemBaseDTO(ImmutableDTO):
    id: UUID
    car_id: UUID
    name: str
    icon: str

    interval_km: int
    interval_days: int
    last_km: int
    last_date: date | None = None
    warn_at: float

    notes: str | None = None
    is_active: bool


class ServiceItemResponseDTO(ImmutableDTO):
    pass
