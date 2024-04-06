# routes.py
from typing import List
import json
import os
import subprocess
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from tempfile import TemporaryDirectory

from .helpers import save_uploaded_images

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