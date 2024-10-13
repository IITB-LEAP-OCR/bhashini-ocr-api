import os
import json
from subprocess import call,check_output
import time
from subprocess import check_output
from typing import List, Tuple

import shutil
import uuid
from os.path import join

from fastapi import UploadFile

from .models import *
from .config import *

def logtime(t: float, msg:  str) -> None:
	print(f'[{int(time.time() - t)}s]\t {msg}')

t = time.time()

def run_docker(image_folder):
    check_output(['docker','run','--rm','--net','host','-v',f'{image_folder}:/data',docker_image_name])

def convert_geometry_to_bbox(
	geometry: Tuple[Tuple[float, float], Tuple[float, float]],
	dim: Tuple[int, int],
	padding: int = 0
) -> BoundingBox:
	"""
	converts the geometry that is fetched from the doctr models
	to the standard bounding box model
	format of the geometry is ((Xmin, Ymin), (Xmax, Ymax))
	format of the dim is (height, width)
	"""
	x1 = int(geometry[0][0] * dim[1])
	y1 = int(geometry[0][1] * dim[0])
	x2 = int(geometry[1][0] * dim[1])
	y2 = int(geometry[1][1] * dim[0])
	return BoundingBox(
		x=x1 - padding,
		y=y1 - padding,
		w=x2-x1 + padding,
		h=y2-y1 + padding,
	)

def process_textron_output(folder_path: str) -> List[LayoutImageResponse]:
    try:
        run_docker(folder_path)
        a = open(folder_path+'/out.json', 'r').read().strip()
        a = json.loads(a)
        ret=[]
        for page in a.keys():
            regions=[]
            for bbox in a[page]:
                regions.insert(0,
                    Region.from_bounding_box(
                        BoundingBox(x=int(bbox['x']),y=int(bbox['y']),w=int(bbox['w']),h=int(bbox['h']),
                            label=bbox['label'],
                        )
					)
                )
            ret.append(
                LayoutImageResponse(
                  image_name=page,
                  regions=regions.copy()
                )
            )
        return ret     
                     
    except Exception as e:
        print(e)

def textron_visualize(image_path: str) -> List[Region]:
    run_docker(image_path)
    a = open(image_path+'/out.json', 'r').read().strip()
    a = json.loads(a)
    for page in a.keys():
        regions=[]
        for bbox in a[page]:
            regions.insert(0,
                Region.from_bounding_box(
                    BoundingBox(x=int(bbox['x']),y=int(bbox['y']),w=int(bbox['w']),h=int(bbox['h']),
                        label=bbox['label'],
                    )
                )
            )
        return regions