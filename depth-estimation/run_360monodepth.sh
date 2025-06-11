#!/bin/bash

WORK_DIR=${1:-data}

# Build image if not already built
docker build -t 360monodepth depth-estimation/.

# Run container and mount $WORK_DIR into the container
docker run -u $(id -u):$(id -g) \
  -e USER=$USER -e XDG_CACHE_HOME=$XDG_CACHE_HOME \
  -v "$(pwd)/$WORK_DIR":/app/data \
  -it --rm 360monodepth \
  python /app/depth-estimation/run.py /app/data/data.txt
