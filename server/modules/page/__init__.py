from fastapi import APIRouter

from .attr.routes import router as attr_router
from .ocr.routes import router as ocr_router
from .layout_detection.routes import router as layout_detect_router
from .layout_preserve.routes import router as layout_preserve_router

router = APIRouter(
    prefix="/page",
    tags=["Page level"]
)

router.include_router(attr_router)
router.include_router(ocr_router)
router.include_router(layout_detect_router)
router.include_router(layout_preserve_router)