from fastapi import APIRouter
from starlette import status

from api.dependencies.services.auth import AuthServiceDepends
from src.types import SignInRequestDTO, SignUpRequestDTO, TokenPairDTO

from src.types.exeptions import ToManyRequestsErrorDTO, HTTPExceptionErrorDTO, IncorrectPasswordErrorDTO

from src.types.user import UserDetailResponseDTO

__all__ = ["router"]

router = APIRouter(tags=["Auth"])


@router.post(
    path="/signup",
    summary="Регистрация",
    response_model=UserDetailResponseDTO,
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    }
)
async def sign_up(data: SignUpRequestDTO, service: AuthServiceDepends) -> UserDetailResponseDTO:
    return await service.sign_up(data=data)


@router.post(
    path="/signin",
    summary="Вход",
    response_model=TokenPairDTO,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": IncorrectPasswordErrorDTO},
        # HTTP_404_NOT_FOUND: {"model": ObjectNotFoundErrorDTO(name="user")},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": ToManyRequestsErrorDTO},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPExceptionErrorDTO},
    },
)
async def sign_in(data: SignInRequestDTO, service: AuthServiceDepends) -> TokenPairDTO:
    return await service.sign_in(data=data)
