# Textron
The module to Detect text from the page level image using textron.
## Load from Docker Hub
```
docker pull shouryatyagi222/textron:1
```
## Docker command used :
```
docker run --rm --net host -v IMAGE_FOLDER:/data textron:1
```
Note: Update the `Docker Container Name` in config.py
### Textron Inference : /api/0.0.1/page/layout/text
### Textron Visualization : /api/0.0.1/page/layout/text/visualize

## Note
1. The Following Module downloads the required doctr models in the build image.
2. Update the docker Image Name in `/bhashini-ocr-api/server/modules/page/textron/config.py` and IMAGE_DIR  in `/bhashini-ocr-api/server/modules/config.py`