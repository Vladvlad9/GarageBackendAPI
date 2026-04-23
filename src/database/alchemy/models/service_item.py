from datetime import date
from typing import List
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, String, Integer, Date, CheckConstraint, Float, Text, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
        UniqueConstraint("car_id", "name", name="uq_service_item_car_name"),
    )
    id: Mapped[UUID] = mapped_column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )
    car_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("car.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(150))  # "Моторное масло"
    icon: Mapped[str] = mapped_column(String(50), default="oil")  # ключ иконки

    # интервал по пробегу (0 = не используется)
    interval_km: Mapped[int] = mapped_column(Integer, default=0)
    # интервал по времени (0 = не используется)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)
    # данные последнего выполнения
    last_km: Mapped[int] = mapped_column(Integer, default=0)
    last_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    # порог предупреждения: 0.75 = показать "Скоро" когда использовано 75% интервала
    warn_at: Mapped[float] = mapped_column(Float, default=0.75)

    # кастомные поля
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    car: Mapped["Car"] = relationship(back_populates="service_items")
    records: Mapped[List["ServiceRecord"]] = relationship(
        back_populates="service_item",
        cascade="all, delete-orphan",
        order_by="ServiceRecord.date.desc()",
    )

    def __repr__(self) -> str:
        return f"<ServiceItem(id={self.id}, name='{self.name}', car_id='{self.car_id}')>"

    def __str__(self) -> str:
        return f"ServiceItem id={self.id}, name={self.name}"
