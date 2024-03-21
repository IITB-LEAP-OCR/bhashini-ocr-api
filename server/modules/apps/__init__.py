from fastapi import APIRouter

from .iitb_v0_ocr.routes import router as apps_ocr_router

router = APIRouter(
    prefix="/apps",
    tags=["Apps level"]
)

router.include_router(apps_ocr_router)
