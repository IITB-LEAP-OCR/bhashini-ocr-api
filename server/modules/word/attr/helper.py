from fastapi import UploadFile

import json
from subprocess import call
from os.path import join
from shutil import copyfileobj

from .models import SIResponse


def save_uploaded_image(image: UploadFile,image_dir) -> str:	
	print(f'Saving {image.filename} to location: {image_dir}')
	location = join(image_dir, f'{image.filename}')
	with open(location, 'wb') as f:
		copyfileobj(image.file, f)
	return image_dir
        
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
            ret = SIResponse(text=loaded[0])
            print(ret)
            return ret
    except:
        print("Error while trying to open output file")

     
def run_docker(IMAGE_FOLDER, docker_image_name):
        # print(IMAGE_FOLDER)
        # try:
        #     check_output(['docker','run','--rm','--net','host','-v',f'{IMAGE_FOLDER}:/model/data',docker_image_name],shell=True)
        # except:
        #     check_output(['sudo', 'docker','run','--rm','--net','host','-v',f'{IMAGE_FOLDER}:/model/data',docker_image_name],shell=True)
        #     # check_output(command)
        call(f'docker run --rm --net host -v {IMAGE_FOLDER}:/model/data {docker_image_name}',shell=True)