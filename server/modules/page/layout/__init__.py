from fastapi import APIRouter

from .text import router as text_router

router = APIRouter(
    prefix="/layout"
)

router.include_router(text_router)