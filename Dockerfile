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
    libgl1-mesa-dev \  # OpenGL libraries
    libglfw3 \         # GLFW for window management
    libglfw3-dev \     # Development files for GLFW
    mesa-utils \       # Utilities for Mesa (OpenGL implementation)
    freeglut3-dev \    # FreeGLUT for managing windows with OpenGL
 && pip3 install --no-cache-dir \
    opencv-python==4.5.2.54 \
    tqdm \
    PyOpenGL \         # Python bindings for OpenGL
    PyOpenGL_accelerate \  # Accelerate module for PyOpenGL
    pygame \           # Python library for writing video games
    numpy \
    plyfile \
    torch \
    matplotlib \
    pyrr \             # Python implementations of 3D mathematics functions
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Set up directories
RUN mkdir -p ./shaders ./data ./images ./output \
 && chmod -R 777 ./shaders ./data ./images ./output

# Copy necessary files
COPY extract_frames.py run_colmap.py trans_to_gaussian_splatt.py process_pipeline.py opengl_renderer.py ./
COPY ./shaders/ ./shaders/
# Optional entrypoint
# COPY docker_entrypoint.sh /app/
# RUN chmod +x /app/docker_entrypoint.sh
# ENTRYPOINT ["/app/docker_entrypoint.sh"]

CMD ["bash"]
