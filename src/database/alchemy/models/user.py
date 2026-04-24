from typing import List
from uuid import uuid4

from sqlalchemy import CheckConstraint, String, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base

__all__ = ["User"]


class User(Base, LifecycleMixin):
    __table_args__ = (
        CheckConstraint(sqltext="length(name) >= 3", name="name_min_length"),
        CheckConstraint(sqltext="length(email) >= 5", name="email_min_length"),
        CheckConstraint(sqltext="email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name="email_format"),
    )
    id: Mapped[UUID] = mapped_column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    cars: Mapped[List["Car"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    # refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
    #     back_populates="user",
    #     cascade="all, delete-orphan",
    # )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"

    def __str__(self) -> str:
        return f"User {self.email}"
