from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base

from src.enums.mileage_log import MileageLogsEnum

__all__ = ["MileageLog"]


class MileageLog(Base, LifecycleMixin):
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

    mileage: Mapped[int] = mapped_column(Integer)
    source: Mapped[MileageLogsEnum] = mapped_column(ENUM(MileageLogsEnum), default=MileageLogsEnum.MANUAL)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    car: Mapped["Car"] = relationship(back_populates="mileage_logs")

    def __repr__(self) -> str:
        return f"<MileageLog(id={self.id}, car_id='{self.car_id}', mileage='{self.mileage}')>"

    def __str__(self) -> str:
        return f"MileageLog id={self.id}"
