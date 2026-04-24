from uuid import UUID

from pydantic import EmailStr

from src.types.base import ImmutableDTO

__all__ = ["UserBaseDTO", "UserResponseIdDTO", "UserDetailResponseDTO"]


class UserResponseIdDTO(ImmutableDTO):
    id: UUID


class UserBaseDTO(ImmutableDTO):
    id: UUID
    name: str
    email: EmailStr
    is_active: bool
    is_verified: bool


class UserDetailResponseDTO(UserBaseDTO):
    pass
