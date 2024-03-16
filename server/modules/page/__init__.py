from fastapi import APIRouter

from .layout import router as layout_router
from .ocr.routes import router as ocr_router

router = APIRouter(
    prefix="/page",
    tags=["Page level"]
)

router.include_router(layout_router)
router.include_router(ocr_router)