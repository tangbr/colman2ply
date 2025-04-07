# Use Ubuntu 20.04 with CUDA if GPU is needed
FROM nvidia/cuda:11.0.3-runtime-ubuntu20.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies + COLMAP + Python
RUN apt-get update && apt-get install -y \
    xvfb \
    colmap \
    python3 \
    python3-pip \
    ffmpeg \
    libgl1-mesa-dev \
    libglfw3 \
    libglfw3-dev \
    mesa-utils \
    freeglut3-dev \
 && pip3 install --no-cache-dir \
    opencv-python==4.5.2.54 \
    tqdm \
    PyOpenGL \
    PyOpenGL_accelerate \
    pygame \
    numpy \
    plyfile \
    torch \
    matplotlib \
    pyrr \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Set up directories
RUN mkdir -p ./shaders ./data ./images ./output \
 && chmod -R 777 ./shaders ./data ./images ./output

# Copy necessary files
COPY extract_frames.py run_colmap.py trans_to_gaussian_splatt.py process_pipeline.py ./
COPY ./shaders/ ./shaders/
# Optional entrypoint
# COPY docker_entrypoint.sh /app/
# RUN chmod +x /app/docker_entrypoint.sh
# ENTRYPOINT ["/app/docker_entrypoint.sh"]

CMD ["bash"]
