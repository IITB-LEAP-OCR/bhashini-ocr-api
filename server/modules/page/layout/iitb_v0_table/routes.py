# routes.py
from typing import List
import json
import os, io
import subprocess
import cv2
from fastapi import APIRouter, UploadFile, Depends, File, Form
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from tempfile import TemporaryDirectory

from .helpers import save_uploaded_images, visualize_bounding_boxes

router = APIRouter(
	prefix='/table'
)


@router.post("")
async def detect_table(images: List[UploadFile]):
    temp = TemporaryDirectory()
    image_path = save_uploaded_images(images, temp.name)

    print("Calling docker")
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

    # Extract message and bboxes from out.json
    message = out.get("message", "Table Detection Successful")
    bboxes = out.get("bboxes", [])

    # Check if table detection was unsuccessful (no bboxes detected)
    if not bboxes:
        message = "No table detected"

    # Construct API response
    response_content = {
        "message": message,
        "bboxes": bboxes
    }

    return JSONResponse(content=response_content)


@router.post("/visualize")
async def visualize_tables(images: List[UploadFile]):
    temp = TemporaryDirectory()
    image_path = save_uploaded_images(images, temp.name)
    print("Image Path:", image_path)

    # Invoke Docker container for table detection
    docker_command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{temp.name}:/model/data",
        "tabledockerizefinal"
    ]
    subprocess.call(docker_command)

    # Load detected bounding boxes from the output JSON file
    with open(os.path.join(temp.name, "out.json")) as f:
        out = json.load(f)
        bboxes = out.get("bboxes", [])

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