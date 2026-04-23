from datetime import date as date_dt
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, Date, Integer, Float, Text, Boolean, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base

__all__ = ["FuelLog"]


class FuelLog(Base, LifecycleMixin):
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

    date: Mapped[date_dt] = mapped_column(Date, index=True)
    mileage: Mapped[int] = mapped_column(Integer)  # пробег при заправке
    liters: Mapped[float] = mapped_column(Float)  # сколько залили
    price_per_liter: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    station: Mapped[str | None] = mapped_column(String(200), nullable=True)
    full_tank: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    car: Mapped["Car"] = relationship(back_populates="fuel_logs")

    __table_args__ = (
        Index("ix_fuel_logs_car_date", "car_id", "date"),
    )

    def __repr__(self) -> str:
        return f"<FuelLog(id={self.id}, car_id='{self.car_id}', mileage='{self.mileage}')>"

    def __str__(self) -> str:
        return f"FuelLog id={self.id}"
