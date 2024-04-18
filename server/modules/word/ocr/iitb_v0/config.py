from ....config import IMAGE_FOLDER
import os


MODEL_FOLDER='/home/ocrdev/ocr-api/temp_models'
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

LANGUAGES = {
	'en': 'english',
	'hi': 'hindi',
	'mr': 'marathi',
	'ta': 'tamil',
	'te': 'telugu',
	'kn': 'kannada',
	'gu': 'gujarati',
	'pa': 'punjabi',
	'bn': 'bengali',
	'ml': 'malayalam',
	'asa': 'assamese',
	'mni': 'manipuri',
	'ori': 'oriya',
	'ur': 'urdu',

	# Extra languages
	'brx': 'bodo',
	'doi': 'dogri',
	'ks': 'kashmiri',
	'kok': 'konkani',
	'mai': 'maithili',
	'ne': 'nepali',
	'sa': 'sanskrit',
	'sat': 'santali',
	'sd': 'sindhi',
}

TESS_LANG = {
	'english': 'eng',
	'hindi': 'hin',
	'marathi': 'mar',
	'tamil': 'tam',
	'telugu': 'tel',
	'kannada': 'kan',
	'gujarati': 'guj',
	'punjabi': 'pan',
	'bengali': 'ben',
	'malayalam': 'mal',
	'assamese': 'asm',
	'manipuri': 'mni',
	'oriya': 'ori',
	'urdu': 'urd',
}