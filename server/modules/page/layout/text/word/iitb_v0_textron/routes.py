import uuid
from typing import List

import io
import cv2
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from tempfile import TemporaryDirectory

from .dependencies import save_uploaded_images
from .models import *
from .helper import *
from .config import *

router = APIRouter(
    prefix=""
)

@router.post('/', response_model=List[LayoutImageResponse])
async def text_detection(
	image: UploadFile = File(...),
	model: ModelChoice = Form(ModelChoice.textron),
):
	"""
	API endpoint for calling the textron text detection
	"""
	temp = TemporaryDirectory()
	print(f"orig_pdf_path.filename: {image.filename}")
	print(f"temp.name: {temp.name}")
	save_uploaded_images([image],temp.name)

	print(model.value)
	if model == ModelChoice.textron:
		ret = process_textron_output(temp.name)
	return ret


@router.post('/visualize')
async def text_detection_visualization(
	image: UploadFile = File(...),
	model: ModelChoice = Form(ModelChoice.textron),
):
	"""
	API endpoint for calling the textron text detection Visualzation
	"""
	temp = TemporaryDirectory()
	print(f"orig_pdf_path.filename: {image.filename}")
	print(f"temp.name: {temp.name}")
	image_path = save_uploaded_images([image],temp.name)
	print(model.value)
	print(image_path)
	if model == ModelChoice.textron:
		regions = textron_visualize(temp.name)

	bboxes = [i.bounding_box for i in regions]
	bboxes = [((i.x, i.y), (i.x+i.w, i.y+i.h)) for i in bboxes]
	img = cv2.imread(image_path)
	count = 1
	for i in bboxes:
		img = cv2.rectangle(img, i[0], i[1], (0,0,255), 2)
	cv2.imwrite(image_path, img)
	with open(image_path, mode="rb") as img_file:
		return StreamingResponse(io.BytesIO(img_file.read()), media_type="image/jpeg")
