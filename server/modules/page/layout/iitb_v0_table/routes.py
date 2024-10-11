# routes.py
from typing import List
import json
import os, io
import subprocess
import cv2
from fastapi import APIRouter, UploadFile, Depends, File, Form
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from tempfile import TemporaryDirectory
from enum import Enum
import ast

from .helpers import save_uploaded_images, visualize_bounding_boxes

router = APIRouter(
	prefix='/table'
)

class Choice(str, Enum):
    frcnn = "frcnn"
    yolo = "yolo"


def get_bboxes_from_model_choice(choice, temp, images):
    bboxes = []
    if choice == Choice.frcnn:
        print("Calling frcnn docker")
        docker_command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{temp.name}:/model/data",
            "tabledockerizefinal"
        ]
        subprocess.call(docker_command)
        print("Done docker")

        with open(os.path.join(temp.name, "out.json")) as f:
            out = json.load(f)

        bboxes = out.get("bboxes", [])
    else:
        print("Calling yolo docker")
        image = images[0]
        cmd = f"docker run --rm --gpus all -it -v {temp.name}/{image.filename}:/docker/uploads/{image.filename} tablecalls uploads/{image.filename} td True > temp.txt"
        os.system(cmd)
        fp = open('temp.txt', 'r')
        lines = fp.readlines()
        result = lines[-1]
        bboxes = ast.literal_eval(result)
        print(bboxes)
        print("Done docker")
    return bboxes



@router.post("")
async def detect_table(
    images: List[UploadFile],
    model: Choice = Form(Choice.frcnn)
    ):
    temp = TemporaryDirectory()
    image_path = save_uploaded_images(images, temp.name)
    print(model)

    bboxes = get_bboxes_from_model_choice(model, temp, images)

    # Check if table detection was unsuccessful (no bboxes detected)
    if not bboxes:
        response_content = {
            "message": 'No Tables Detected',
            "bboxes": []
        }

    else:
        # Construct API response
        response_content = {
            "message": 'Table Detection Successful',
            "bboxes": bboxes
        }

    return JSONResponse(content=response_content)


@router.post("/visualize")
async def visualize_tables(
    images: List[UploadFile],
    model: Choice = Form(Choice.frcnn)
    ):
    temp = TemporaryDirectory()
    image_path = save_uploaded_images(images, temp.name)
    print("Image Path:", image_path)
    print(model)
    bboxes = get_bboxes_from_model_choice(model, temp, images)

    # Visualize bounding boxes on the input image
    annotated_image = visualize_bounding_boxes(os.path.join(image_path, images[0].filename), bboxes)
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




"""

@router.post("/graphics/equation")
async def detect_equation(images: List[UploadFile]):
    temp = TemporaryDirectory()
    image_path = save_uploaded_images(images, temp.name)

    print("Calling docker")
    docker_command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{temp.name}:/model/data",
        "page-layout"
    ]
    subprocess.call(docker_command)
    print("Done docker")

    with open(os.path.join(temp.name, "out.json")) as f:
        out = json.load(f)

    # Extract tables and cells from the output JSON
    equations = out.get("equations", [])

    return JSONResponse(content={"message": "Equation Detection Successful", "layout": {"equations": equations}})


@router.post("/graphics/photo")
async def detect_figure(images: List[UploadFile]):
    temp = TemporaryDirectory()
    image_path = save_uploaded_images(images, temp.name)

    print("Calling docker")
    docker_command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{temp.name}:/model/data",
        "page-layout"
    ]
    subprocess.call(docker_command)
    print("Done docker")

    with open(os.path.join(temp.name, "out.json")) as f:
        out = json.load(f)

    # Extract tables and cells from the output JSON
    figures = out.get("figures", [])

    return JSONResponse(content={"message": "Figure Detection Successful", "layout": {"figures": figures}})


"""