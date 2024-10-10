from fastapi import APIRouter, Body, File, UploadFile
from .helper import *
import subprocess
from .models import TSRResponse
from tempfile import TemporaryDirectory
import os

router = APIRouter(
	prefix='/table'
)

@router.post(
        '',
        response_model = TSRResponse,
        response_model_exclude_none = True)

async def get_tsr(
    image: UploadFile = File(...),
    struct_flag: bool = Body(...),
    )-> TSRResponse:
    
    try:
        # Create a temporary directory
        temp = TemporaryDirectory()

        print(f"orig_path.filename: {image.filename}")
        print(f"temp.name: {temp.name}")
        save_uploaded_images([image],temp.name)
        print(f"Struct_Flag: {struct_flag}")

        print("Calling docker")
        docker_command = [
            "sudo",
            "docker",
            "run",
            "--rm",
            # "--gpus",
            # "all",
            "-it",
            "-v",
            f"{temp.name}/{image.filename}:/docker/uploads/{image.filename}",
            "tablecalls",
            f"uploads/{image.filename}",
            "tsr",
            f"{struct_flag}"
            # ">",
            # f"{temp.name}/temp.txt"
        ]
        # subprocess.call(docker_command)

        result = subprocess.Popen(docker_command, stdout = subprocess.PIPE)
        for line in result.stdout:
            print(line)
        print("Done docker")

        # with open(os.path.join(temp.name,"temp.txt")) as fp:
        #     lines = fp.readlines()
        #     #struct_cells = lines[-2][:-1]
        #     html = lines[-1][:-1]
        #     print('+++++++++++++++++')
        #     print(html)

        # Return OCRResponse using the results
        return TSRResponse(result_message = f'TSR SUCCESSFUL', result_html = 'html')
    except Exception as e:
        # If an exception occurs, return an OCRResponse with an error message
        return TSRResponse(result_message = f'TSR FAILED: {str(e)}', result_html='')
    finally:
        # Clean up the temporary directory
        temp.cleanup()