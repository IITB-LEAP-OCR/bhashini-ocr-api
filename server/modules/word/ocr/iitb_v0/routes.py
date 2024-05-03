from subprocess import check_output
import os

from fastapi import APIRouter, Request, Depends

from .helper import *
from .models import OCRRequest, OCRResponse
from .config import *
from tempfile import TemporaryDirectory
from .dependencies import save_uploaded_images

router = APIRouter(
    prefix=''
)

@router.post('/', response_model=OCRResponse)
async def infer_ocr_2(
	image: UploadFile = File(...),
	modality: ModalityEnum = Form(ModalityEnum.printed),
	language: LanguageEnum = Form(LanguageEnum.hi),
):

	temp = TemporaryDirectory()

	print(f"orig_pdf_path.filename: {image.filename}")
	print(f"temp.name: {temp.name}")
	
	save_uploaded_images([image],temp.name)

	modality = modality.value
	lcode = language
	try:
		if len(os.listdir(MODEL_FOLDER))==0:
			download_models_from_file(models_txt_path,MODEL_FOLDER)
	except:
		return "Error in Downloading the models , try Updating the models_txt_path in .s/bhashini-ocr-api/server/modules/word/ocr/iitb_v0/config.py"

	if modality=='handwritten':
		check_output(['docker','run','--rm','--net','host','-v',f'{temp.name}:/data','-v',f'{MODEL_FOLDER}:/models','-v',f'{MODEL_FOLDER}:/root/.cache/doctr/models',DOCKER_NAME,'python','infer.py','-l',lcode,'-t',modality])
		ret = process_ocr_output(lcode, modality, temp.name)
		print(ret)
		return ret
	if modality=='printed':
		check_output(['docker','run','--rm','--net','host','-v',f'{temp.name}:/data','-v',f'{MODEL_FOLDER}:/models','-v',f'{MODEL_FOLDER}:/root/.cache/doctr/models',DOCKER_NAME,'python','infer.py','-l',lcode,'-t',modality])
		ret = process_ocr_output(lcode, modality, temp.name)
		return ret