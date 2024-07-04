FROM python:3.11.4

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y\
    && apt-get clean

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .