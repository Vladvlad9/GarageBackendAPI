from datetime import timedelta

from orjson import dumps, loads
from redis.asyncio import Redis

from src.config import async_redis_client
from src.utils.jwt import IncorrectJWTBanPayloadError, JWTStorageUnavailableError

__all__ = ["JWTStorage"]


class JWTStorage:
    storage_backend: Redis = async_redis_client

    @classmethod
    def generate_key(cls, key: str, prefix: str) -> str:
        return f"jwt_ban:{prefix}:{key}"

    @classmethod
    async def set(cls, key: str, value: dict | str, exp: int | timedelta | None) -> None:
        try:
            await cls.storage_backend.set(name=key, value=dumps(value), ex=exp)
        except Exception:
            raise JWTStorageUnavailableError()

    @classmethod
    async def get(cls, key: str) -> dict | str | None:
        try:
            payload = await cls.storage_backend.get(key)
        except Exception:
            raise JWTStorageUnavailableError()
        else:
            if payload:
                try:
                    return loads(payload)
                except Exception:
                    raise IncorrectJWTBanPayloadError()
            return None
