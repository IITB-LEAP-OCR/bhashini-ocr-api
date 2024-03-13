from fastapi import APIRouter

from tempfile import TemporaryDirectory

from .helper import *
from .models import *

router = APIRouter(
    prefix='/attr'
)

@router.post(
    '/script',
    response_model=list[SIResponse],
    response_model_exclude_none=True
)
def identify_script(si_request: PostprocessRequest, model: ModelChoice, venv_path = "layout-parser-venv", si_venv_path = "server/modules/script_identification/layout-parser-venv-script-identification") -> list[SIResponse]:
    """
    This is an endpoint for identifying the script of the word images.
    this model was contributed by **Punjab university (@Ankur)** on 07-10-2022
    The endpoint takes a list of images in base64 format and outputs the
    identified script for each image in the same order.

    Currently 8 recognized languages are [**hindi, telugu, tamil, gujarati,
    punjabi, urdu, bengali, english**]

    API inputs a list of images in base64 encoded string and outputs a list
    of objects containing **"text"** as key and **language** as value
    """
    tmp = TemporaryDirectory(prefix='st_script')
    process_images(si_request.images, tmp.name)
    if(model==ModelChoice.default):
        call(f'./script_iden_v1.sh {tmp.name}', shell=True)
        ret = process_layout_output(tmp.name)
    elif(model==ModelChoice.alexnet):
        run_docker(tmp.name, "script-identification")	
        ret = process_output(tmp.name)
    return ret