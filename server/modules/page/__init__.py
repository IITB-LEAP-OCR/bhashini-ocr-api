from fastapi import APIRouter

from .layout import router as layout_router

router = APIRouter(
    prefix="/page",
    tags=["Page level"]
)

router.include_router(layout_router)