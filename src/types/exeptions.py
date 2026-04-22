from typing import Literal

from src.types.base import ImmutableDTO


class ToManyRequestsErrorDTO(ImmutableDTO):
    detail: Literal["to_many_requests"] = "to_many_requests"

class HTTPExceptionErrorDTO(ImmutableDTO):
    detail: str = "something_went_wrong"

class IncorrectPasswordErrorDTO(ImmutableDTO):
    detail: Literal["incorrect_password"] = "incorrect_password"