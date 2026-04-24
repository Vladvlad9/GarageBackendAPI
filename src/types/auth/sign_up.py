from pydantic import EmailStr

from src.types.annotaed import PasswordStr
from src.types.base import ImmutableDTO

__all__ = ["SignUpRequestDTO"]


# пределать name

class SignUpRequestDTO(ImmutableDTO):
    name: str
    email: EmailStr
    password: PasswordStr
