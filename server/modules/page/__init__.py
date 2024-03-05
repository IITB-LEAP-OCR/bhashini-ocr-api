from fastapi import APIRouter

from .attr.routes import router as attr_router
from .ocr.routes import router as ocr_router

router = APIRouter(
    prefix="/page",
    tags=["Page level"]
)

router.include_router(attr_router)
router.include_router(ocr_router)