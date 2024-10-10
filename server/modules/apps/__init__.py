from fastapi import APIRouter

from .iitb_v0_ocr.routes import router as apps_ocr_router
from .iitb_v1_table.routes import router as apps_table_router

router = APIRouter(
    prefix="/apps",
    tags=["Apps level"]
)

router.include_router(apps_ocr_router)
router.include_router(apps_table_router)
