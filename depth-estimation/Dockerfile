# Base image with CUDA 12.3 and Ubuntu 20.04
FROM nvidia/cuda:12.3.0-devel-ubuntu20.04

# Noninteractive mode and timezone setup
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

# Update and install core system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    cmake \
    libeigen3-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libopencv-dev \
    libceres-dev \
    python3-pybind11 \
    git \
    wget \
    libboost1.71-dev \
    libpython3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /monodepth

# Copy the 360monodepth folder (from depth-estimation build context)
COPY 360monodepth ./360monodepth

# Download MiDaS model weights
RUN mkdir -p ./360monodepth/BoostingMonocularDepth/midas && \
    wget https://github.com/isl-org/MiDaS/releases/download/v2_1/model-f6b98070.pt -O ./360monodepth/BoostingMonocularDepth/midas/model.pt

RUN find ./360monodepth -name "requirements.txt" -type f
RUN ls -la ./360monodepth/

# Install Python dependencies
RUN ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install colorama>=0.4.4 matplotlib>=3.4.1 scikit-image>=0.18.1 scipy>=1.6.2 opencv-python>=4.5.1.48 torch>=1.8.1 torchvision>=0.9.1 wheel>=0.36.2 packaging>=20.0 pyparsing>=2.3.1 "numpy<2,>=1.20" pillow>=6.2.0 timm==0.6.13

RUN cd ./360monodepth/code/cpp && mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j

# Give full read-write access to monodepth files
RUN chmod -R a+rwX /monodepth

# Optional: HuggingFace cache directory
ENV HF_HOME /monodepth/cache

# Default command: launch a bash shell
CMD ["/bin/bash"]