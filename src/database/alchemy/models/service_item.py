from datetime import date
from typing import List
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, String, Integer, Date, CheckConstraint, Float, Text, Boolean, UniqueConstraint, \
    case, func, text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, query_expression, column_property

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models import Car
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

    car: Mapped[Car] = relationship(back_populates="service_items")
    records: Mapped[List["ServiceRecord"]] = relationship(
        back_populates="service_item",
        cascade="all, delete-orphan",
        order_by="ServiceRecord.date.desc()",
    )

    car_mileage = column_property((
        select(Car.mileage)
        .where(Car.id == car_id)
        .correlate_except(Car)
        .scalar_subquery()
    ))

    # сколько проехали
    km_used = column_property(func.greatest(
        0,
        func.coalesce(car_mileage, 0) - last_km,
    ))

    # сколько дней прошло
    days_used = column_property(
        func.greatest(
            0,
            func.current_date() - last_date,
        )
    )

    # ===== PROGRESS (как на фронте) =====
    progress = column_property(
        case(
            # km приоритет
            (
                interval_km > 0,
                func.least(
                    1.0,
                    func.greatest(
                        0,
                        func.coalesce(car_mileage, 0) - last_km
                    ) / func.nullif(interval_km, 0),
                ),
            ),

            # days fallback
            (
                (interval_days > 0) & (last_date.isnot(None)),
                func.least(
                    1.0,
                    func.greatest(
                        0,
                        func.current_date() - last_date
                    ) / func.nullif(interval_days, 0),
                ),
            ),

            else_=0.0,
        )
    )

    # ===== OVERDUE =====
    is_overdue = column_property(
        case(
            (
                interval_km > 0,
                func.greatest(
                    0,
                    func.coalesce(car_mileage, 0) - last_km
                ) >= interval_km,
            ),
            (
                (interval_days > 0) & (last_date.isnot(None)),
                func.greatest(
                    0,
                    func.current_date() - last_date
                ) >= interval_days,
            ),
            else_=False,
        )
    )

    # ===== NEEDS ATTENTION =====
    needs_attention = column_property(
        case(
            (
                interval_km > 0,
                (
                        func.greatest(
                            0,
                            func.coalesce(car_mileage, 0) - last_km
                        ) / func.nullif(interval_km, 0)
                ) >= warn_at,
            ),
            (
                (interval_days > 0) & (last_date.isnot(None)),
                (
                        func.greatest(
                            0,
                            func.current_date() - last_date
                        ) / func.nullif(interval_days, 0)
                ) >= warn_at,
            ),
            else_=False,
        )
    )

    # ===== NEXT KM =====
    next_due_km = column_property(
        case(
            (
                interval_km > 0,
                last_km + interval_km,
            ),
            else_=None,
        )
    )

    # ===== NEXT DATE =====
    next_due_date = column_property(
        case(
            (
                (interval_days > 0) & (last_date.isnot(None)),
                last_date + interval_days * text("interval '1 day'"),
            ),
            else_=None,
        )
    )

    def __repr__(self) -> str:
        return f"<ServiceItem(id={self.id}, name='{self.name}', car_id='{self.car_id}')>"

    def __str__(self) -> str:
        return f"ServiceItem id={self.id}, name={self.name}"

# ServiceItem.initialize()
