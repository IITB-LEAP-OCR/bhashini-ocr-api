# bhashini-ocr-api Inference


## Word-Level OCR Inference Instructions


1. Create and Activate the new environment
2. ``` pip install -r requirements.txt```
3. Ensure to check *config.py* file for all the data paths and configurations
4. Run ```python infer.py``` by providing the correct paraments, example is given for reference
5. Example code with parameters ```python infer.py -l hi -t printed -m crnn_vgg16_bn -v all``` 


## Word-Level OCR Inference through Docker
This repository contains the code that takes in `IMAGE_FOLDER`, `MODEL_FOLDER` as parameter for docker run and processes the images to get the textual Content of the Image.

## Building the Image
```
docker build -t iitb-ocr .
```
## Inference using the docker container
```
docker run --rm --gpus all --net host \
    -v MODEL_DIR:/root/.cache/doctr/models \
	-v MODEL_DIR:/models \
	-v DATA_DIR:/data \
	DOCKER_NAME \
	python infer.py -l LANGUAGE -t MODALITY
```
Where,
- MODEL_DIR: path to the models folder.
- DATA_DIR: path to the Image folder.
- DOCKER_NAME: name of you docker container.
- LANGUAGE: Name of the Language for the OCR.
- MODALITY: Printed/Handwritten.

### Example
```
docker run --rm -v /home/ocrdev/ocr-api/temp_models:/root/.cache/doctr/models -v /home/ocrdev/ocr-api/temp_models:/models -v /home/ocrdev/ocr-api/testimages/word_level:/data iitb-ocr:2 python infer.py -t handwritten -l hi
```