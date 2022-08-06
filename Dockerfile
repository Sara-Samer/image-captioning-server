# Specify your base image
# FROM python:3.7.3-stretch
FROM --platform=linux/x86_64 python:3.9
# FROM --platform=linux/aarch64 python:3.9
# FROM --platform=linux/arm64 python:3.8
# create a work directory
RUN mkdir /app
# navigate to this work directory
WORKDIR /app
#Copy all files
COPY . .
# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN pip install https://github.com/diyor28/tf-docker-m1/releases/download/v1.0.0/tensorflow-2.8.0-cp39-cp39-linux_aarch64.whl
RUN pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.html
# Run
CMD ["python","upload.py"]
