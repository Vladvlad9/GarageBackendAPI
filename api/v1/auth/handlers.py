from fastapi import APIRouter

from src.types import SignInRequestDTO, SignUpRequestDTO, TokenPairDTO

__all__ = ["router"]

router = APIRouter(tags=["Auth"])


@router.post(
    path="/signup",
    summary="Регистрация",
    response_model=None,

)
async def sign_up(data: SignInRequestDTO) -> None:
    pass


@router.post(
    path="/signin",
    summary="Вход",
    response_model=TokenPairDTO,

)
async def sign_in(data: SignUpRequestDTO) -> TokenPairDTO:
    pass
