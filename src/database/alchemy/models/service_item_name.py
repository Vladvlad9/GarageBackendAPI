from uuid import uuid4

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.alchemy.models.base import Base

__all__ = ["ServiceItemName"]


class ServiceItemName(Base):
    id: Mapped[UUID] = mapped_column(
        UUID,
        insert_default=uuid4,
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(150))  # "Моторное масло"
    icon: Mapped[str] = mapped_column(String(50), default="oil")  # ключ иконки

    service_item: Mapped["ServiceItem"] = relationship(
        back_populates="service_item_name"
    )

    def __repr__(self) -> str:
        return f"<ServiceItemName(id={self.id}, name='{self.name}', icon='{self.icon}')>"

    def __str__(self) -> str:
        return f"ServiceItemName id={self.id}, name={self.name}, icon='{self.icon}"