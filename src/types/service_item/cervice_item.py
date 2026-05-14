from datetime import date
from uuid import UUID

from src.types.base import ImmutableDTO

from src.types.service_item_name import ServiceItemNameBase

__all__ = ["ServiceItemResponseDTO", "ServiceItemBaseDTO", "ServiceItemCreateDTO", "ServiceItemCoreDTO"]


class ServiceItemBaseDTO(ImmutableDTO):
    id: UUID
    car_id: UUID
    service_item_name: ServiceItemNameBase

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


class ServiceItemCoreDTO(ImmutableDTO):
    id: UUID
    car_id: UUID
    service_item_name_id: UUID

    interval_km: int
    interval_days: int
    last_km: int
    last_date: date | None = None
    warn_at: float | None

    notes: str | None = None
    is_active: bool


class ServiceItemResponseDTO(ImmutableDTO):
    pass


class ServiceItemCreateDTO(ImmutableDTO):
    car_id: UUID
    service_item_name_id: UUID
    last_km: int
    last_date: date
