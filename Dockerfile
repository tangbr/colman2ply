# Use Ubuntu 22.04 (Jammy) so we can install COLMAP from apt
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y xvfb  # Install xvfb

# Install system dependencies + COLMAP + Python
RUN apt-get update && apt-get install -y xvfb colmap python3 python3-pip ffmpeg libgl1-mesa-dev libglfw3 libglfw3-dev mesa-utils freeglut3-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages for frame extraction scripts
RUN pip3 install --no-cache-dir opencv-python tqdm PyOpenGL PyOpenGL_accelerate pygame numpy plyfile torch

# Create a working directory
WORKDIR /app

RUN mkdir -p /shaders

COPY extract_frames.py run_colmap.py trans_to_gaussian_splatt.py ./

COPY shaders/ ./shaders/

# (Optional) If you want an entrypoint script
# COPY docker_entrypoint.sh /app/docker_entrypoint.sh
# RUN chmod +x /app/docker_entrypoint.sh
# ENTRYPOINT ["/app/docker_entrypoint.sh"]

# Default command (example: run your Python scripts)
CMD ["bash"]
