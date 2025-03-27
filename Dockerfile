# Use Ubuntu 22.04 (Jammy) so we can install COLMAP from apt
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies + COLMAP + Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    colmap \
    python3 \
    python3-pip \
    ffmpeg \
    # (Optional) other tools you might need
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages for frame extraction scripts
RUN pip3 install --no-cache-dir opencv-python tqdm

# Create a working directory
WORKDIR /app

# Copy your scripts
COPY extract_frames.py run_colmap.py ./

# (Optional) If you want an entrypoint script
# COPY docker_entrypoint.sh /app/docker_entrypoint.sh
# RUN chmod +x /app/docker_entrypoint.sh
# ENTRYPOINT ["/app/docker_entrypoint.sh"]

# Default command (example: run your Python scripts)
CMD ["bash"]
