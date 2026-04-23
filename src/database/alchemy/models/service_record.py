from datetime import date as date_dt
from typing import Optional
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, String, Date, Integer, Float, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base

__all__ = ["ServiceRecord"]


class ServiceRecord(Base, LifecycleMixin):
    id: Mapped[UUID] = mapped_column(
        UUID,
        primary_key=True,
        insert_default=uuid4,
    )
    car_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("car.id", ondelete="CASCADE"),
        index=True,
    )
    service_item_id: Mapped[UUID | None] = mapped_column(
        UUID,
        ForeignKey("service_item.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # данные записи
    name: Mapped[str] = mapped_column(String(150))  # дублируем на случай удаления service_item
    date: Mapped[date_dt] = mapped_column(Date, index=True)
    mileage_at_service: Mapped[int] = mapped_column(Integer)  # пробег в момент ТО

    # детали
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)  # стоимость
    workshop: Mapped[str | None] = mapped_column(String(200), nullable=True)  # СТО / мастер
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_service_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    next_service_date: Mapped[date_dt | None] = mapped_column(Date, nullable=True)

    car: Mapped["Car"] = relationship(back_populates="service_records")
    service_item: Mapped[Optional["ServiceItem" ]] = relationship(back_populates="records")

    __table_args__ = (
        Index("ix_service_records_car_date", "car_id", "date"),
    )

    def __repr__(self) -> str:
        return f"<ServiceRecord {self.name} {self.date}>"

    def __str__(self) -> str:
        return f"ServiceRecord id={self.id}, name={self.name}"
