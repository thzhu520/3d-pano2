#!/bin/bash

WORK_DIR=${1:-data}

# Build container
docker build -t 3d-photo-inpainting inpainting/.

# Run container with the working dir mounted
docker run --runtime=nvidia -u $(id -u):$(id -g) \
  -e USER=$USER \
  -v "$(pwd)/$WORK_DIR":/app/data \
  -it --rm 3d-photo-inpainting \
  python /app/inpainting/time.py /app/data
