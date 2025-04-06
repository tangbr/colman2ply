#!/bin/bash
set -e

# If you pass arguments like "my_video.mp4", it will be in "$1".
VIDEO_PATH="$1"
USERNAME="$2"

if [[ -z "$VIDEO_PATH" || -z "$USERNAME" ]]; then
    echo "Usage: docker run ... /path/to/video username"
    exit 1
fi


echo "🔹 Running extract_frames.py on: $VIDEO_PATH"
python3 /app/extract_frames.py --video "$VIDEO_PATH" --out /app/images --step 10

echo "Running run_colmap.py"
python3 /app/run_colmap.py --images /app/images --out /app/output

echo "✅ Completed processing for user: $USERNAME"
echo "🎯 PLY model located at: /app/output/model.ply"
# Optional: If you want to open the .ply with MeshLab automatically:
# meshlab /app/sparse/0/model.ply
# or wherever your model file is located.

# exec "$@"
