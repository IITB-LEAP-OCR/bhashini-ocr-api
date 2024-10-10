from fastapi import APIRouter, Body, File, UploadFile
from .helper import *
import subprocess
from .models import TSRResponse
from fastapi.responses import StreamingResponse
from tempfile import TemporaryDirectory
import os, io
import ast

router = APIRouter(
	prefix='/table'
)

@router.post(
        '',
        response_model = TSRResponse,
        response_model_exclude_none = True)

async def get_tsr(
    image: UploadFile = File(...),
    structure_only: bool = Body(...),
    )-> TSRResponse:
    
    try:
        # Create a temporary directory
        temp = TemporaryDirectory()
        print(f"orig_path.filename: {image.filename}")
        print(f"temp.name: {temp.name}")
        save_uploaded_images([image],temp.name)
        print(f"Struct_Flag: {structure_only}")
        print("Calling docker")
        cmd = f"docker run --rm --gpus all -it -v {temp.name}/{image.filename}:/docker/uploads/{image.filename} tablecalls uploads/{image.filename} tsr {structure_only} > temp.txt"
        os.system(cmd)
        fp = open('temp.txt', 'r')
        lines = fp.readlines()
        struct_cells = lines[-2][:-1]
        html = lines[-1][:-1]
        print(struct_cells)
        print(html)
        print("Done docker")
        return TSRResponse(result_message = f'TSR SUCCESSFUL', result_html = html)
    except Exception as e:
        # If an exception occurs, return an OCRResponse with an error message
        return TSRResponse(result_message = f'TSR FAILED: {str(e)}', result_html='')
    finally:
        # Clean up the temporary directory
        temp.cleanup()


@router.post(
        '/visualize',
        response_model = TSRResponse,
        response_model_exclude_none = True)

async def visualize_tsr(image: UploadFile = File(...))-> TSRResponse:
    
    # Create a temporary directory
    temp = TemporaryDirectory()
    print(f"orig_path.filename: {image.filename}")
    print(f"temp.name: {temp.name}")
    image_path = save_uploaded_images([image],temp.name)
    print("Calling docker")
    cmd = f"docker run --rm --gpus all -it -v {temp.name}/{image.filename}:/docker/uploads/{image.filename} tablecalls uploads/{image.filename} tsr True > temp.txt"
    os.system(cmd)
    fp = open('temp.txt', 'r')
    lines = fp.readlines()
    struct_cells = lines[-2][:-1]
    print(struct_cells)
        # Visualize bounding boxes on the input image
    annotated_image = visualize_bounding_boxes(os.path.join(image_path, image.filename), ast.literal_eval(struct_cells))
    print("Annotated Image Size:", annotated_image.shape)

    # Save the annotated image
    print("Temp name:", temp.name)
    annotated_image_path = os.path.join(image_path, "annotated_image.jpg")
    try:
        cv2.imwrite(annotated_image_path, annotated_image)
        print("Saved image at:", annotated_image_path)
    except Exception as e:
        print("Error saving annotated image:", e)

    # Return annotated image as response
    with open(annotated_image_path, mode="rb") as img_file:
        return StreamingResponse(io.BytesIO(img_file.read()), media_type="image/jpeg")
