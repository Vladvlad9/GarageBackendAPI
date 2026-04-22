from uuid import uuid4

from sqlalchemy import CheckConstraint, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.database.alchemy.mixins import LifecycleMixin
from src.database.alchemy.models.base import Base

__all__ = ["Account"]


class Account(Base, LifecycleMixin):
    __table_args__ = (
        CheckConstraint(sqltext="length(email) >= 5", name="email_min_length"),
        CheckConstraint(sqltext="email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name="email_format"),
    )
    id: Mapped[UUID] = mapped_column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )

    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=True)

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, email='{self.email}')>"

    def __str__(self) -> str:
        return f"Account {self.email}"
