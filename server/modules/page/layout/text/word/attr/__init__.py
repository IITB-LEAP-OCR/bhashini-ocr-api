from fastapi import APIRouter

from .iitb_v0.routes import get_font_properties_from_image as get_font_properties_from_image_iitb_v0

router = APIRouter(
    prefix="/attr"
)

router.post("/style")(get_font_properties_from_image_iitb_v0)