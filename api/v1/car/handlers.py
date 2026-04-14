from fastapi import APIRouter

router = APIRouter(tags=["Car"])


@router.get("/")
async def testa():
    pass
