from shutil import copyfileobj
from os.path import join

from fastapi import UploadFile

def save_uploaded_image(image: UploadFile,image_dir) -> str:	
	print(f'Saving {image.filename} to location: {image_dir}')
	location = join(image_dir, f'{image.filename}')
	with open(location, 'wb') as f:
		copyfileobj(image.file, f)
	return image_dir