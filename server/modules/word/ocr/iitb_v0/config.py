import os

MODEL_FOLDER='/home/ocrdev/ocr-api/temp_models'
DOCKER_NAME="iitb-ocr"
models_txt_path="./bhashini-ocr-api/server/modules/word/ocr/iitb_ocr_models.txt"

	
try:
	if not os.path.exists(MODEL_FOLDER):
		os.mkdir(MODEL_FOLDER)
except Exception as e:
	print('Error :',e)
	print('Update the Path to the IITB Word OCR Models Folder in ./bhashini-ocr-api/server/modules/word/ocr/iitb_v0/config.py')

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