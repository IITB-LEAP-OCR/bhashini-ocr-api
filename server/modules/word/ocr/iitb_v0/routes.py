from subprocess import check_output
import os

from fastapi import APIRouter, Request, Depends

from .helper import *
from .models import OCRRequest, OCRResponse
from .config import *
from .dependencies import save_uploaded_images

router = APIRouter(
    prefix=''
)

@router.post('/', response_model=OCRResponse)
async def infer_ocr_2(
	folder_path: str = Depends(save_uploaded_images),
	modality: ModalityEnum = Form(ModalityEnum.printed),
	language: LanguageEnum = Form(LanguageEnum.hi),
):

	modality = modality.value
	lcode = language
	if len(os.listdir(MODEL_FOLDER))==0:
		download_models_from_file(models_txt_path,MODEL_FOLDER)

	if modality=='handwritten':
		check_output(['docker','run','--rm','--net','host','-v',f'{IMAGE_FOLDER}:/data','-v',f'{MODEL_FOLDER}:/models','-v',f'{MODEL_FOLDER}:/root/.cache/doctr/models',DOCKER_NAME,'python','infer.py','-l',lcode,'-t',modality])
		ret = process_ocr_output(lcode, modality, IMAGE_FOLDER)
		print(ret)
		return ret
	if modality=='printed':
		check_output(['docker','run','--rm','--net','host','-v',f'{IMAGE_FOLDER}:/data','-v',f'{MODEL_FOLDER}:/models','-v',f'{MODEL_FOLDER}:/root/.cache/doctr/models',DOCKER_NAME,'python','infer.py','-l',lcode,'-t',modality])
		ret = process_ocr_output(lcode, modality, IMAGE_FOLDER)
		return ret