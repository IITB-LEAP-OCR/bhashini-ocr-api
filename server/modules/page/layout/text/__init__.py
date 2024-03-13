from fastapi import APIRouter

from .word import router as word_router

router = APIRouter(
    prefix="/text"
)

router.include_router(word_router)