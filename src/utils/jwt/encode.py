from jwt import encode

from settings import settings
from src.types import TokenPayload


__all__ = ["JWTEncodeMixin"]


class JWTEncodeMixin:
    @classmethod
    async def encode(cls, payload: TokenPayload, key: str, algorithm: str) -> str:
        return encode(
            payload=payload,
            key=key,
            algorithm=algorithm,
        )

    @classmethod
    async def encode_access_token(cls, payload: TokenPayload) -> str:
        return await cls.encode(
            payload=payload,
            key=settings.JWT.ACCESS_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT.ACCESS_ALGORITHM,
        )

    @classmethod
    async def encode_refresh_token(cls, payload: TokenPayload) -> str:
        return await cls.encode(
            payload=payload,
            key=settings.JWT.REFRESH_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT.REFRESH_ALGORITHM,
        )