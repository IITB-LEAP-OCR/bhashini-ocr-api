# routes.py
from typing import List
import json
import os
import subprocess
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from tempfile import TemporaryDirectory

from server.modules.page.layout.helpers import save_uploaded_images

router = APIRouter(
	prefix='/layout'
)


@router.post("/table")
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
        "page-layout"
    ]
    subprocess.call(docker_command)
    print("Done docker")

    with open(os.path.join(temp.name, "out.json")) as f:
        out = json.load(f)

    # Extract tables and cells from the output JSON
    tables = out.get("tables", [])
    cells = out.get("cells", [])

    return JSONResponse(content={"message": "Table Detection Successful", "layout": {"tables": tables, "cells": cells}})







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