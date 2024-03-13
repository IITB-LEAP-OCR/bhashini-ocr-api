from subprocess import check_output
import os

from fastapi import APIRouter, Request

from .helper import *
from .models import OCRRequest, OCRResponse
from .config import *

router = APIRouter(
	prefix='/api/0.0.1/word',
	tags=['IITB Models'],
)

@router.post(
	'/ocr',
	response_model=OCRResponse,
	response_model_exclude_none=True
)
async def infer_ocr(
	ocr_request: OCRRequest, 
	request: Request
) -> OCRResponse:
	
	process_images(ocr_request.image)
	lcode, language, modality, dlevel = process_config(ocr_request.config)

	if len(os.listdir(MODEL_FOLDER))==0:
		download_models_from_file(models_txt_path,MODEL_FOLDER)

	if modality=='handwritten':
		check_output(['docker','run','--rm','--net','host','-v',f'{IMAGE_FOLDER}:/data','-v',f'{MODEL_FOLDER}:/models','-v',f'{MODEL_FOLDER}:/root/.cache/doctr/models',DOCKER_NAME,'python','infer.py','-l',lcode,'-t',modality])
		# call(f'./infer_iitb_v2.sh {modality} {lcode} {IMAGE_FOLDER} {MODEL_FOLDER} {DOCKER_NAME}', shell=True)
		ret = process_ocr_output(lcode, modality, IMAGE_FOLDER)
		return ret
	if modality=='printed':
		check_output(['docker','run','--rm','--net','host','-v',f'{IMAGE_FOLDER}:/data','-v',f'{MODEL_FOLDER}:/models','-v',f'{MODEL_FOLDER}:/root/.cache/doctr/models',DOCKER_NAME,'python','infer.py','-l',lcode,'-t',modality])
		# call(f'./infer_iitb_v2.sh {modality} {lcode} {IMAGE_FOLDER} {MODEL_FOLDER} {DOCKER_NAME}', shell=True)
		ret = process_ocr_output(lcode, modality, IMAGE_FOLDER)
		return ret
