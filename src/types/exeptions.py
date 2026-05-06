from typing import Literal

from pydantic import Field
from starlette import status

from src.types.base import ImmutableDTO


class ObjectNotFoundErrorDTO(ImmutableDTO):
    detail: str = Field(default="object_not_found", pattern=r"^[a-z_]+_not_found$")

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not name:
            raise ValueError("Name cannot be empty")

        detail = f"{name}_not_found"

        super().__init__(detail=detail)


class ObjectAlreadyExistErrorDTO(ImmutableDTO):
    detail: str = Field(default="object_already_exists", pattern=r"^[a-z_]+_already_exists$")

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not name:
            raise ValueError("Name cannot be empty")

        detail = f"{name}_already_exists"

        super().__init__(detail=detail)


class ToManyRequestsErrorDTO(ImmutableDTO):
    detail: Literal["to_many_requests"] = "to_many_requests"


class HTTPExceptionErrorDTO(ImmutableDTO):
    detail: str = "something_went_wrong"


class IncorrectPasswordErrorDTO(ImmutableDTO):
    detail: Literal["incorrect_password"] = "incorrect_password"


class InvalidTokenOrExpiredException(ImmutableDTO):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UnauthorizedErrorDTO().detail
        )

class UnauthorizedErrorDTO(ImmutableDTO):
    detail: Literal["unauthorized"] = "unauthorized"
