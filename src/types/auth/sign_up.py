from pydantic import EmailStr, model_validator

from src.types.annotaed import PasswordStr
from src.types.base import ImmutableDTO

__all__ = ["SignUpRequestDTO"]


# пределать name

class SignUpRequestDTO(ImmutableDTO):
    name: str
    email: EmailStr
    password: PasswordStr
    confirm: PasswordStr

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.confirm:
            raise ValueError('password and confirm must match')
        return self
