import base64
import imghdr
import json
import os
import shutil
from datetime import datetime
from os.path import join
from tempfile import TemporaryDirectory
from subprocess import call
from typing import List
from uuid import uuid4

import pytz
import requests
from fastapi import HTTPException
from PIL import Image
import re

from .models import *
from .config import *

def download_models_from_file(file_path, output_folder):
    call(f'wget -i {file_path} -P {output_folder}',shell=True)

def process_image_content(image_content: str, savename: str, savefolder: str) -> None:
	"""
	input the base64 encoded image and saves the image inside the folder.
	savename is the name of the image to be saved as
	"""
	print('received image as base64')
	assert isinstance(image_content, str)
	with open(join(savefolder, savename), 'wb') as f:
		f.write(base64.b64decode(image_content))

def process_images(image_content, image_folder):
	"""
	processes all the images in the given list.
	"""
	print('deleting all the previous data from the images folder')
	os.system(f'rm -rf {image_folder}/*')
	if image_content:
		for idx, image_file in enumerate(image_content):
			try:
				process_image_content(image_file, '{}.jpg'.format(idx), image_folder)
			except:
				raise HTTPException(
					status_code=400,
					detail='Error while decodeing and saving the image #{}'.format(idx)
				)
	else:
		raise HTTPException(
			status_code=400,
			detail='Image Not Found'
		)

def process_config(config: OCRRequest):
	global LANGUAGES
	try:
		language_code = config.language.value
		modality = config.modality.value
	except Exception as e:
		print(e)
		raise HTTPException(
			status_code=400,
			detail='language code is either not present or invalid'
		)
	return (language_code, modality)


def process_ocr_output(language_code: str, modality: str, image_folder: str) -> OCRResponse:
	try:
		with open(os.path.join(image_folder, 'out.json'), 'r') as file:
			data = json.load(file)

		data = [i for i in data.split('\n') if len(i)>0]
		response = OCRResponse(output=data, status=200)
		print('ocr output :', response)

	except FileNotFoundError:
		response = OCRResponse(output=["File Not Found"], status=404)

	except Exception as e:
		response = OCRResponse(output=[e], status=500)  # Internal server error status

	return response