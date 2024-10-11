from fastapi import APIRouter, Body, File, UploadFile
from .helper import *
import subprocess
from .models import OCRResponse
from tempfile import TemporaryDirectory
import os
import pickle
import json

router = APIRouter(
	prefix='/page'
)

@router.post(
        '/lpo',
        response_model = OCRResponse,
        response_model_exclude_none=True)

async def get_lpo(
    image: UploadFile = File(...),
    project_folder_name: str = Body(...),
    language: str = Body(...),
    equation: bool = Body(...),
    figure: bool = Body(...),
    table: bool = Body(...)
    )-> OCRResponse:
    
    try:
        # Create a temporary directory
        temp = TemporaryDirectory()

        print(f"orig_pdf_path.filename: {image.filename}")
        print(f"temp.name: {temp.name}")
        
        
        save_uploaded_images([image],temp.name)

        # Set layout_preservation based on equation, figure, and table
        layout_preservation = equation or figure or table

        print(f"Equation: {equation}, Figure: {figure}, Table: {table}, Layout Preservation: {layout_preservation}")

        # If all three parameters are False, set them to True
        if not equation and not figure and not table:
            equation = figure = table = True
            layout_preservation = True
            print(f"Revised values: Equation: {equation}, Figure: {figure}, Table: {table}, Layout Preservation: {layout_preservation}")


        # Build configuration dictionary
        config = {
            "orig_pdf_path": os.path.join("data", image.filename),
            "project_folder_name": project_folder_name,
            "lang": language,
            "equation": equation,
            "figure": figure,
            "table": table,
            "ocr_only": True,
            "layout_preservation": layout_preservation,
            "nested_ocr": False
        }

        # Serialize and save configuration to a file
        with open(os.path.join(temp.name, "config"), "wb") as f:
            pickle.dump(config, f)

        print("Calling docker")
        docker_command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{temp.name}:/model/data",
            "layoutpreserve"
        ]
        subprocess.call(docker_command)
        print("Done docker")


        with open(os.path.join(temp.name,"output.json")) as f:
            output = json.load(f)
        response = output

        # Return OCRResponse using the results
        return OCRResponse(**response)
    except Exception as e:
        # If an exception occurs, return an OCRResponse with an error message
        return OCRResponse(result_message=f'OCR FAILED: {str(e)}', result_html='')
    finally:
        # Clean up the temporary directory
        temp.cleanup()


@router.post(
        '/reconstruct',
        response_model = OCRResponse,
        response_model_exclude_none = True)

async def get_table_text_ocr(
    image: UploadFile = File(...),
    )-> OCRResponse:
    
    try:
        # Create a temporary directory
        temp = TemporaryDirectory()
        print(f"orig_path.filename: {image.filename}")
        print(f"temp.name: {temp.name}")
        save_uploaded_images([image],temp.name)
        print("Calling docker")
        cmd = f"docker run --rm --gpus all -it -v {temp.name}/{image.filename}:/docker/uploads/{image.filename} tablecalls uploads/{image.filename} tr True > temp.txt"
        os.system(cmd)
        fp = open('temp.txt', 'r')
        lines = fp.readlines()
        full_logs = ''.join(lines)
        start = full_logs.find('<?xml version="1.0" encoding="UTF-8"?>')
        html = full_logs[start:]
        print("Done docker")
        return OCRResponse(result_message = f'OCR SUCCESSFUL', result_html = html)
    except Exception as e:
        # If an exception occurs, return an OCRResponse with an error message
        return OCRResponse(result_message = f'OCR FAILED: {str(e)}', result_html='')
    finally:
        # Clean up the temporary directory
        temp.cleanup()
        os.system('rm temp.txt')