from pydantic import SecretStr

from settings._base import BaseSettingsConfig

__all__ = ["JWTSettings"]


class JWTSettings(BaseSettingsConfig, env_prefix="JWT_"):
    ACCESS_SECRET_KEY: SecretStr
    REFRESH_SECRET_KEY: SecretStr

    ACCESS_PUBLIC_KEY: SecretStr
    REFRESH_PUBLIC_KEY: SecretStr

    ACCESS_EXP_TIME: int
    REFRESH_EXP_TIME: int
    ACCESS_ALGORITHM: str
    REFRESH_ALGORITHM: str
