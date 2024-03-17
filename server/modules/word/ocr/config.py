from ...config import IMAGE_FOLDER
import os


MODEL_FOLDER='/home/ocrdev/ISHAN/Shourya_dkrimg/models'
DOCKER_NAME="iitb-ocr"
models_txt_path="/home/ocrdev/ISHAN/bhashini-ocr-api/server/modules/word/ocr/iitb_ocr_models.txt"

if not os.path.exists(MODEL_FOLDER):
	os.mkdir(MODEL_FOLDER)
	
try:
	if not os.path.exists(IMAGE_FOLDER):
		os.mkdir(IMAGE_FOLDER)
	if not os.path.exists(MODEL_FOLDER):
		os.mkdir(MODEL_FOLDER)
except Exception as e:
	print('Error :',e)