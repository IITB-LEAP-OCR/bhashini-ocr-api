import os
import shutil
import cv2
from typing import List
from os.path import join
from fastapi import UploadFile


def delete_files_in_directory(directory_path):
   try:
     files = os.listdir(directory_path)
     for file in files:
       file_path = os.path.join(directory_path, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

def save_uploaded_images(images: List[UploadFile],image_dir) -> str:
	print('removing all the previous uploaded files from the image folder')
	delete_files_in_directory(image_dir)
	print(f'Saving {len(images)} to location: {image_dir}')
	for image in images:
		location = join(image_dir, f'{image.filename}')
		with open(location, 'wb') as f:
			shutil.copyfileobj(image.file, f)
	return image_dir

# Function to visualize detected bounding boxes on the input image
def visualize_bounding_boxes(image_path: str, bboxes: list):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to read the input image.")
        return None

    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        print("Bounding Box Coordinates:", x1, y1, x2, y2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image