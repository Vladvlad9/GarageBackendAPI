from datetime import date
from uuid import UUID

from pydantic import model_validator

from src.types.base import ImmutableDTO

__all__ = ["ServiceItemResponseDTO", "ServiceItemBaseDTO"]


class ServiceItemBaseDTO(ImmutableDTO):
    id: UUID
    car_id: UUID
    service_item_name_id: UUID
    # icon: str

    interval_km: int
    interval_days: int
    last_km: int
    last_date: date | None = None
    warn_at: float

    notes: str | None = None
    is_active: bool

    progress: float
    is_overdue: bool
    needs_attention: bool

    next_due_km: int | None
    next_due_date: date | None


class ServiceItemResponseDTO(ImmutableDTO):
    pass
