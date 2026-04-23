from typing import List
from uuid import uuid4

from sqlalchemy import UUID, CheckConstraint, ForeignKey, String, Integer, Float, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base

__all__ = ["Car"]

from src.enums.car import TransmissionEnum, FuelTypeEnum


class Car(Base, LifecycleMixin):
    __table_args__ = (
        CheckConstraint("year >= 1900", name="car_year_valid"),
        CheckConstraint("mileage >= 0", name="car_mileage_positive"),
        CheckConstraint("length(name) > 0", name="car_name_not_empty"),
        Index("ix_cars_user_archived", "user_id", "is_archived"),
    )

    id: Mapped[UUID] = mapped_column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
    )
    # основные данные
    name: Mapped[str] = mapped_column(String(150))  # "Toyota Camry"
    brand: Mapped[str | None] = mapped_column(String(100))  # "Toyota"
    model: Mapped[str | None] = mapped_column(String(100))  # "Camry"
    year: Mapped[int] = mapped_column(Integer)
    mileage: Mapped[int] = mapped_column(Integer, default=0)  # текущий пробег, км
    color: Mapped[str] = mapped_column(String(20), default="#4a9eff")  # hex цвет в UI

    # дополнительные данные
    vin: Mapped[str | None] = mapped_column(String(17), unique=True, nullable=True)
    license_plate: Mapped[str | None] = mapped_column(String(20), nullable=True)
    engine_volume: Mapped[float | None] = mapped_column(Float, nullable=True)  # 2.0

    fuel_type: Mapped[FuelTypeEnum | None] = mapped_column(ENUM(FuelTypeEnum), nullable=True)
    transmission: Mapped[TransmissionEnum | None] = mapped_column(ENUM(TransmissionEnum), nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(back_populates="cars")
    service_items: Mapped[List["ServiceItem"]] = relationship(
        back_populates="car",
        cascade="all, delete-orphan",
        order_by="ServiceItem.name",
    )
    service_records: Mapped[List["ServiceRecord"]] = relationship(
        back_populates="car",
        cascade="all, delete-orphan",
        order_by="ServiceRecord.date.desc()",
    )
    mileage_logs: Mapped[List["MileageLog"]] = relationship(
        back_populates="car",
        cascade="all, delete-orphan",
        order_by="MileageLog.recorded_at.desc()",
    )
    fuel_logs: Mapped[List["FuelLog"]] = relationship(
        back_populates="car",
        cascade="all, delete-orphan",
        order_by="FuelLog.date.desc()",
    )

    def __repr__(self) -> str:
        return f"<Car(id={self.id}, name='{self.name}', year='{self.year}')>"

    def __str__(self) -> str:
        return f"Car id={self.id}, name={self.name}"
