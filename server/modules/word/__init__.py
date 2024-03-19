from fastapi import APIRouter

from .attr.routes import router as attr_router
from .ocr import router as ocr_router

router = APIRouter(
    prefix="/word",
    tags=["Word level"]
)

router.include_router(attr_router)
router.include_router(ocr_router)