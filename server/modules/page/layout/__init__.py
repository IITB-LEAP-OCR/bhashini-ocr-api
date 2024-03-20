from fastapi import APIRouter

from .text import router as text_router
from .iitb_v0_table.routes import router as table_router

router = APIRouter(
    prefix="/layout"
)

router.include_router(text_router)
router.include_router(table_router)