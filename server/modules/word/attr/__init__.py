from fastapi import APIRouter

from .iitb_v0.routes import identify_script as identify_script_iitb_v0

router = APIRouter(
    prefix="/attr"
)

router.post("/script")(identify_script_iitb_v0)