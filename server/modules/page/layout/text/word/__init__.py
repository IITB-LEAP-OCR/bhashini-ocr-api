from fastapi import APIRouter

from .attr import router as attr_router
from .iitb_v0_textron.routes import router as textron_router

router = APIRouter(
    prefix="/word"
)

router.include_router(attr_router)
router.include_router(textron_router)