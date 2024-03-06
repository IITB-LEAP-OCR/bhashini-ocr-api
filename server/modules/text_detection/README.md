# Textron

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
The Following Module downloads the required doctr models in the build image.