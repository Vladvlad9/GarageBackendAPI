from typing import AnyStr
from bcrypt import checkpw, gensalt, hashpw

__all__ = ['PasswordManager']


class PasswordManager:
    SALT_ROUNDS: int = 12
    SALT_PREFIX: bytes = b"2b"

    @classmethod
    def hash(cls, plain_password: AnyStr) -> str:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode()

        return hashpw(
            password=plain_password,
            salt=gensalt(rounds=cls.SALT_ROUNDS, prefix=cls.SALT_PREFIX),
        ).decode()

    @classmethod
    def check(cls, plain_password: AnyStr, password_hash: AnyStr) -> bool:
        if isinstance(plain_password, str):
            plain_password = plain_password.encode()

        if isinstance(password_hash, str):
            password_hash = password_hash.encode()

        return checkpw(password=plain_password, hashed_password=password_hash)
