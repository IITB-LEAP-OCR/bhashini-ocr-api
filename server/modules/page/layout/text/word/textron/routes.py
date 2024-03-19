import uuid
from typing import List

import cv2
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse

from .dependencies import save_uploaded_images
from .models import *
from .helper import *
from .config import *

router = APIRouter(
    prefix=""
)

@router.post('/', response_model=List[LayoutImageResponse])
async def text_detection(
	folder_path: str = Depends(save_uploaded_images),
	model: ModelChoice = Form(ModelChoice.textron),
):
	"""
	API endpoint for calling the textron text detection
	"""
	print(model.value)
	if model == ModelChoice.textron:
		ret = process_textron_output(folder_path)
	# if dilate:
	# 	ret = process_multiple_dilate(ret)
	return ret


@router.post('/visualize')
async def text_detection_visualization(
	image: UploadFile = File(...),
	model: ModelChoice = Form(ModelChoice.textron),
):
	"""
	API endpoint for calling the textron text detection Visualzation
	"""
	image_path = save_uploaded_image(image)
	print(model.value)
	print(image_path)
	if model == ModelChoice.textron:
		regions = textron_visualize(image_path)

	# if dilate:
	# 	regions = process_dilate(regions, image_path)
	save_location = '{}/{}.jpg'.format(
		IMAGE_FOLDER,str(uuid.uuid4())
	)
	# TODO: all the lines after this can be transfered to the helper.py file
	bboxes = [i.bounding_box for i in regions]
	bboxes = [((i.x, i.y), (i.x+i.w, i.y+i.h)) for i in bboxes]
	img = cv2.imread(image_path)
	count = 1
	for i in bboxes:
		img = cv2.rectangle(img, i[0], i[1], (0,0,255), 2)
	cv2.imwrite(save_location, img)
	return FileResponse(save_location)
