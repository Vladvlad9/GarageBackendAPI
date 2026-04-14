from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, String, Integer, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base

__all__ = ["ServiceItem"]


class ServiceItem(Base, LifecycleMixin):
    __table_args__ = (
        CheckConstraint("interval_km >= 0", name="interval_km_positive"),
        CheckConstraint("last_km >= 0", name="last_km_positive"),
        CheckConstraint("interval_days >= 0", name="interval_days_positive"),
        CheckConstraint("length(name) > 0", name="service_name_not_empty"),
        CheckConstraint("(interval_km > 0 OR interval_days > 0)", name="at_least_one_interval"),
        CheckConstraint("last_date IS NULL OR last_date <= CURRENT_DATE", name="last_date_in_past"),
    )
    id: Mapped[UUID] = mapped_column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )
    car_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("car.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(String)
    interval_km: Mapped[int] = mapped_column(Integer, default=0)
    last_km: Mapped[int] = mapped_column(Integer, default=0)
    last_date: Mapped[Date] = mapped_column(Date, nullable=True)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return f"<ServiceItem(id={self.id}, name='{self.name}', car_id='{self.car_id}')>"

    def __str__(self) -> str:
        return f"ServiceItem id={self.id}, name={self.name}"
