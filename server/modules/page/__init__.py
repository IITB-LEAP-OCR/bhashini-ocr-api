from fastapi import APIRouter

from .layout_preserve.routes import router as layout_preserve_router

router = APIRouter(
    prefix="/page",
    tags=["Page level"]
)

router.include_router(layout_preserve_router)