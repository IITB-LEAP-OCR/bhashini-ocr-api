from fastapi import APIRouter

router = APIRouter(
    prefix="/ocr"
)

@router.get("/test")
async def test():
    return "Tested"