from jwt import decode

from settings import settings
from src.types import TokenPayload
from src.utils.jwt import DecodeError

__all__ = ["JWTDecodeMixin"]


class JWTDecodeMixin:
    @classmethod
    async def decode(cls, token: str, key: str, algorithms: list[str]) -> TokenPayload:
        try:
            return TokenPayload(**decode(jwt=token, key=key, algorithms=algorithms))
        except Exception:
            raise DecodeError()

    @classmethod
    async def decode_access_token(cls, token: str) -> TokenPayload:
        try:
            return await cls.decode(
                token=token,
                key=settings.JWT.ACCESS_PUBLIC_KEY.get_secret_value(),
                algorithms=[settings.JWT.ACCESS_ALGORITHM],
            )
        except Exception as e:
            print(f"JWT decode error: {str(e)}")
            raise DecodeError()

    @classmethod
    async def decode_refresh_token(cls, token: str) -> TokenPayload:
        return await cls.decode(
            token=token,
            key=settings.JWT.REFRESH_PUBLIC_KEY.get_secret_value(),
            algorithms=[settings.JWT.REFRESH_ALGORITHM],
        )
