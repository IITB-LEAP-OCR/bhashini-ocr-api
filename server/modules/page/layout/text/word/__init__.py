from fastapi import APIRouter

from .attr.routes import router as attr_router

router = APIRouter(
    prefix="/word"
)

router.include_router(attr_router)