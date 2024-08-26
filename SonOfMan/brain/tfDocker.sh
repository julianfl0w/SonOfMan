#!/bin/bash

# Set the image name
IMAGE_NAME="tensorflow/tensorflow:latest-gpu"

# Get the current working directory
CURRENT_DIR=$(pwd)

# Run the TensorFlow Docker container with the specified options
docker run --gpus all --net=host -v "$CURRENT_DIR:/app" -it $IMAGE_NAME
