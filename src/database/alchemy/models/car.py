from uuid import uuid4

from sqlalchemy import UUID, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base

__all__ = ["Car"]


class Car(Base, LifecycleMixin):
    __table_args__ = (
        CheckConstraint("year >= 1900", name="car_year_valid"),
        CheckConstraint("mileage >= 0", name="car_mileage_positive"),
        CheckConstraint("length(name) > 0", name="car_name_not_empty")
    )

    id: Mapped[UUID] = mapped_column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    mileage: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"<Car(id={self.id}, name='{self.name}', year='{self.year}')>"

    def __str__(self) -> str:
        return f"Car id={self.id}, name={self.name}"
