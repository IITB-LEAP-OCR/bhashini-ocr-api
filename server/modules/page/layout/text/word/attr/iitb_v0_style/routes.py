import json
import os
import pickle
import cv2
from fastapi import UploadFile, Form
from fastapi.responses import Response
from subprocess import call
from tempfile import TemporaryDirectory

from fastapi import APIRouter

from .models import ModelChoice, TaskChoice, FontAttributeImage
from .helper import save_uploaded_image


router = APIRouter(
    prefix="/attr"
)

@router.post("/style")
async def get_font_properties_from_image(
	image: UploadFile,
	model: ModelChoice = Form(ModelChoice.doctr),
	task: TaskChoice = Form(TaskChoice.attributes),
	k_size: int = Form(default=4),
	bold_threshold: float = Form(default=0.3)
	):
	"""
	This endpoint returns the font attributes of text from images. [Note: Font size only available in tesseract implementation]
	"""
	temp = TemporaryDirectory()
	image_path = save_uploaded_image(image,temp.name)
	
	config = {
		"model": "doctr" if model == ModelChoice.doctr else "tesseract",
		"k_size": k_size,
		"bold_threshold": bold_threshold
	}	

	with open(os.path.join(image_path,"config"),"wb") as f:
		pickle.dump(config,f)

	print("Calling docker")
	# model_dir = os.path.join(os.getcwd(),"models")
	# call(f"docker run --rm -v {temp.name}:/model/data -v{model_dir}:/root/.cache/doctr/models textattrib")
	call(f"docker run --rm -v {temp.name}:/model/data textattrib", shell= True)
	print("Done docker")
	
	if task == TaskChoice.attributes:
		with open(os.path.join(temp.name,"out.json")) as f:
			print("path of out.json = ",os.path.join(temp.name,"out.json"))
			out = json.load(f)
		
		response = FontAttributeImage.model_validate(out)

	
	else:
		result_image = [os.path.join(temp.name,i) for i in os.listdir(os.path.join(temp.name)) if "result" in i][0]
		print("Result image path:", result_image)
		img = cv2.imread(result_image)
		res, im_png = cv2.imencode(".png", img)

		response = Response(content=im_png.tobytes(),media_type="image/png")
	
	temp.cleanup()
	return response