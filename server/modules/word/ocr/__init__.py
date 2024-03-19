from fastapi import APIRouter

from .iitb_v0.routes import router as iitb_v0_router

router = APIRouter(
    prefix="/ocr",
    tags=["Word level"]
)

router.include_router(iitb_v0_router)