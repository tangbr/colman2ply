# Start with Ubuntu 18.04
FROM ubuntu:18.04

# Avoid interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    cmake \
    ninja-build \
    build-essential \
    libboost-all-dev \
    libceres-dev \
    libsuitesparse-dev \
    libfreeimage-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libglew-dev \
    libcgal-dev \
    libatlas-base-dev \
    libflann-dev \
    libeigen3-dev \
    libsqlite3-dev \
    libpng-dev \
    libjpeg-dev \
    libx11-dev \
    mesa-common-dev \
    libglu1-mesa-dev \
    libxrandr-dev \
    qtbase5-dev \
    qtdeclarative5-dev \
    qttools5-dev \
    qtbase5-dev-tools \
    wget \
    ffmpeg \
    python3 \
    python3-pip \
    python3-opencv \
    libmetis-dev \
    python3-setuptools \
    python3-wheel \
    python3-distutils \
    meshlab \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir setuptools wheel scikit-build tqdm && \
    pip3 install --no-cache-dir opencv-python

# Clone COLMAP (do not remove METIS lines so it can link properly)
RUN git clone https://github.com/colmap/colmap.git /colmap && \
    sed -i 's/freeimage::FreeImage/FreeImage/g' /colmap/cmake/FindFreeImage.cmake

# Build and install COLMAP
WORKDIR /colmap/build
RUN rm -rf * && \
    cmake .. -DCUDA_ENABLED=OFF -DCMAKE_VERBOSE_MAKEFILE=ON && \
    make -j"$(nproc)" > /tmp/make_output.log 2>&1 || (cat /tmp/make_output.log && false) && \
    make install

# Copy your scripts into /app
WORKDIR /app
COPY extract_frames.py run_colmap.py ./

# Make python point to python3 for consistent usage.
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy an entrypoint script that will handle runtime args
COPY docker_entrypoint.sh /app/docker_entrypoint.sh
RUN chmod +x /app/docker_entrypoint.sh

# Use the entrypoint script by default
ENTRYPOINT ["/app/docker_entrypoint.sh"]

CMD ["/app/data/my_video.mp4", "default_user"]

