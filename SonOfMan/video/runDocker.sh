#docker run --name resnet_container --rm -v $(pwd):/app resnet_visualizer
SCRIPT_DIR="$(dirname "$0")"
docker run --gpus all --name resnet_container --rm -v "$SCRIPT_DIR":/app resnet_visualizer python classify.py
