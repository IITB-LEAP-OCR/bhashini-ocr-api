from fastapi import APIRouter, UploadFile

from tempfile import TemporaryDirectory

from .helper import save_uploaded_image, run_docker, process_output
from .models import SIResponse

router = APIRouter(
    prefix='/attr'
)

@router.post(
    '/script',
    response_model= SIResponse
)
def identify_script(si_request: UploadFile) -> SIResponse:

    tmp = TemporaryDirectory()
    save_uploaded_image(si_request, tmp.name)

    run_docker(tmp.name, "script-identification")	
    ret = process_output(tmp.name)
    return ret