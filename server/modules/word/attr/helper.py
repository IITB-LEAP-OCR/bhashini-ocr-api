import base64
import json
import os
from subprocess import call
from os.path import join

from fastapi import HTTPException

from .models import SIResponse, ClassifyResponse


def process_images(images: list[str], path: str='/home/layout/layout-parser/images'):
    """
    processes all the images in the given list.
    it saves all the images in the /home/ocr/website/images folder and
    returns this absolute path.
    """
    print('deleting all the previous data from the images folder')
    os.system(f'rm -rf {path}/*')
    for idx, image in enumerate(images):
        if image is not None:
            try:
                # saving the base64 image as JPEG
                assert isinstance(image, str)
                with open(join(path, f'{idx}.jpg'), 'wb') as f:
                    f.write(base64.b64decode(image))
            except:
                raise HTTPException(
                    status_code=400,
                    detail=f'Error while decoding and saving the image #{idx}',
                )
        else:
            raise HTTPException(
                status_code=400,
                detail=f'image #{idx} doesnt contain either imageContent or imageUri',
            )
        
def process_output(path: str = "server/modules/script_identification/output.json"):
    """Processes output.json and returns in response format

    Args:
        path (str, optional): Path to output.json. Defaults to "server/modules/script_identification/output.json".

    Returns:
        List[SIResponse]: Processed output
    """
    try:
        with open(join(path, "output.json"), 'r') as json_file:
            loaded=json.load(json_file)
            print(loaded)
            ret = [SIResponse(text=i) for i in loaded]
            print(ret)
            return ret
    except:
        print("Error while trying to open output file")

def process_layout_output(
	path: str = '/home/layout/layout-parser/images'
) -> list[ClassifyResponse]:
	"""
	process the ./images/out.json file and returns the ocr response.
	"""
	try:
		a = open(join(path, 'out.json'), 'r').read().strip()
		a = json.loads(a)
		a = list(a.items())
		a = sorted(a, key=lambda x:int(x[0].split('.')[0]))
		return [ClassifyResponse(text=i[1]) for i in a]
	except Exception as e:
		print(e)
		raise HTTPException(
			status_code=500,
			detail='Error while parsing the ocr output'
		)
     
def run_docker(IMAGE_FOLDER, docker_image_name):
        # print(IMAGE_FOLDER)
        # try:
        #     check_output(['docker','run','--rm','--net','host','-v',f'{IMAGE_FOLDER}:/model/data',docker_image_name],shell=True)
        # except:
        #     check_output(['sudo', 'docker','run','--rm','--net','host','-v',f'{IMAGE_FOLDER}:/model/data',docker_image_name],shell=True)
        #     # check_output(command)
        call(f'docker run --rm --net host -v {IMAGE_FOLDER}:/model/data {docker_image_name}',shell=True)