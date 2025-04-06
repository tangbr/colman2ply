# Use Ubuntu 22.04 (Jammy) as the base image
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
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
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Python packages for frame extraction and other scripts
RUN pip3 install --no-cache-dir opencv-python tqdm PyOpenGL PyOpenGL_accelerate pygame numpy plyfile torch

# Create a working directory
WORKDIR /app

# Copy your Python scripts from the Dockerfile directory to the container
COPY extract_frames.py run_colmap.py trans_to_gaussian_splatt.py ./ 

# Copy the shaders directory from two levels up to the container
COPY ../../shaders/ ./shaders/

# Optional: Set up an entrypoint script if needed
# COPY docker_entrypoint.sh /app/docker_entrypoint.sh
# RUN chmod +x /app/docker_entrypoint.sh
# ENTRYPOINT ["/app/docker_entrypoint.sh"]

# Default command to run when starting the container
CMD ["bash"]
