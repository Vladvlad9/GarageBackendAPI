from abc import ABC
from typing import TypeVar, Generic, Any, Sequence

from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)

__all__ = ["BaseRepo"]


class BaseRepo(ABC, Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self._session = session
        self._model = model

    async def get(self, filters: list[Any], options: list[Any] | None = None) -> ModelType:
        statement = select(self._model).filter(*filters)
        if options:
            statement = statement.options(*options)

        return await self._session.scalar(statement)

    async def insert(self, obj: dict) -> ModelType:
        try:
            statement = insert(self._model).values(**obj).returning(self._model)
            result = await self._session.execute(statement)
            await self._session.commit()
            return result.scalar_one_or_none()
        except Exception as err:
            print(err)

    async def update(self, filters: list[Any], obj: dict) -> ModelType:
        result = await self._session.execute(
            statement=update(self._model).filter(*filters).values(**obj).returning(self._model)
        )
        await self._session.commit()
        return result.scalar_one_or_none()

    async def delete(self, filters: list[Any]) -> None:
        statement = delete(self._model).filter(*filters).returning(self._model)
        await self._session.execute(statement)
        await self._session.commit()

    async def count(self, filters: list[Any] | None = None) -> int:
        statement = select(func.count(self._model.id))
        if filters:
            statement = statement.filter(*filters)
        return await self._session.scalar(statement=statement)

    async def list_data(
            self,
            page: int,
            page_size: int,
            optional: list[Any] | None = None,
            filters: list[Any] | None = None
    ) -> Sequence[Any | ModelType]:
        statement = select(self._model)
        if optional:
            statement = statement.options(*optional)
        if filters:
            statement = statement.filter(*filters)

        statement = statement.offset(page * page_size - page_size).limit(page_size)
        results = await self._session.scalars(statement=statement)
        return results.unique().all()

    async def add_flush_refresh_one(self, obj: dict) -> ModelType:
        statement = insert(self._model).values(**obj).returning(self._model)
        result = await self._session.execute(statement)
        await self._session.flush()
        return result.scalar_one_or_none()

    async def soft_delete(self, filters: list[Any], obj: dict) -> None:
        statement = update(self._model).filter(*filters).values(**obj)
        await self._session.execute(statement)
        await self._session.commit()
