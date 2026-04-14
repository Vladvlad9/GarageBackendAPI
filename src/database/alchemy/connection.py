from collections.abc import AsyncIterator
from uuid import uuid4

from pydantic.v1.networks import MultiHostDsn
from sqlalchemy import URL, NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

__all__ = ["AlchemyDBConnection"]


class AlchemyDBConnection:
    def __init__(self, url: MultiHostDsn | URL | str):
        self._url = url
        self.engine: AsyncEngine = create_async_engine(
            url=self._url,
            pool_recycle=0,
            poolclass=NullPool,
            query_cache_size=0,
            connect_args={
                "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
                "statement_cache_size": 0,
                "prepared_statement_cache_size": 0,
                "command_timeout": 30,
            },
            execution_options={"isolation_level": "READ COMMITTED"},
        )
        self.session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_maker() as session:
            yield session

    async def close(self) -> None:
        await self.engine.dispose()
