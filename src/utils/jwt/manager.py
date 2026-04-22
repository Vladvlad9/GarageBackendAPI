from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from settings import settings
from src.enums import JWTPrefix

from src.exeptions import TokenIsBannedError
from src.types import TokenPayload
from src.utils.datetime import now
from src.utils.jwt import JWTDecodeMixin, JWTEncodeMixin, JWTStorage


__all__ = ["JWTManager"]


class JWTManager(JWTEncodeMixin, JWTDecodeMixin):
    storage: JWTStorage = JWTStorage
    jti_generator: Callable[[], str] = lambda: f"{uuid4()}"
    JWT_ACCESS_EXP_TIME: timedelta = timedelta(minutes=settings.JWT.ACCESS_EXP_TIME)
    JWT_REFRESH_EXP_TIME: timedelta = timedelta(minutes=settings.JWT.REFRESH_EXP_TIME)

    @classmethod
    async def create_access_token(
        cls,
        user_id: str,
        jti: str,
    ) -> str:
        payload = TokenPayload(
            sub=f"{user_id}",
            iat=now(),
            exp=now() + cls.JWT_ACCESS_EXP_TIME,
            jti=jti,
        )
        return await cls.encode_access_token(payload)

    @classmethod
    async def create_refresh_token(
        cls,
        user_id: str,
        jti: str,
    ) -> str:
        payload = TokenPayload(
            sub=user_id,
            iat=now(),
            exp=now() + cls.JWT_REFRESH_EXP_TIME,
            jti=f"{jti}",
        )
        return await cls.encode_refresh_token(payload)

    @classmethod
    async def create_token_pair(cls, user_id: str | UUID) -> dict[str, str]:
        if isinstance(user_id, UUID):
            user_id = f"{user_id}"

        jti = cls.jti_generator()

        return {
            "access_token": await cls.create_access_token(user_id=user_id, jti=jti),
            "refresh_token": await cls.create_refresh_token(user_id=user_id, jti=jti),
        }

    @classmethod
    async def ban_token_pair(
        cls,
        payload: TokenPayload,
        **kwargs,
    ) -> None:
        iat = payload.get("iat")
        if isinstance(iat, int | float):
            iat = datetime.fromtimestamp(iat, tz=UTC)

        await cls.storage.set(
            key=cls.storage.generate_key(key=payload.get("jti"), prefix=JWTPrefix.JTI),
            value={**kwargs, "jwt_jti": payload.get("jti")},
            exp=iat + timedelta(minutes=settings.JWT.REFRESH_EXP_TIME) - now(),
        )

    @classmethod
    async def ban_all_user_tokens(
        cls,
        user_id: str,
    ) -> None:
        await cls.storage.set(
            key=cls.storage.generate_key(key=user_id, prefix=JWTPrefix.SUB),
            value=now().isoformat(),
            exp=timedelta(minutes=settings.JWT.REFRESH_EXP_TIME),
        )

    @classmethod
    async def is_token_banned(cls, payload: TokenPayload) -> bool:
        last_logout = await cls.storage.get(cls.storage.generate_key(key=payload.get("sub"), prefix=JWTPrefix.SUB))
        if last_logout:
            return datetime.fromtimestamp(payload.get("iat"), tz=UTC) <= datetime.fromisoformat(last_logout)
        if await JWTStorage.get(key=JWTStorage.generate_key(key=payload.get("jti"), prefix=JWTPrefix.JTI)):
            raise TokenIsBannedError()
        return False