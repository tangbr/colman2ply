import cv2
import os
import argparse
from tqdm import tqdm
import shutil

def safe_directory_clear(directory):
    """Attempt to clear all contents of a directory safely."""
    try:
        shutil.rmtree(directory)
        os.makedirs(directory)  # Recreate the directory after clearing
    except OSError as e:
        print(f"Warning: Failed to remove directory {directory} - {e}")
        # If the directory removal fails, try to remove all files inside it
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

def extract_frames(video_path, output_dir, step=10, clean_start=False):
    """Extracts frames from a video file, optionally clearing the output directory first."""
    if clean_start:
        safe_directory_clear(output_dir)
    else:
        os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count, saved_count = 0, 0

    with tqdm(total=total_frames) as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % step == 0:
                filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
                cv2.imwrite(filename, frame)
                saved_count += 1
            frame_count += 1
            pbar.update(1)

    cap.release()
    print(f"✅ Extracted {saved_count} frames to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Path to input video")
    parser.add_argument("--out", default="images", help="Output directory for extracted frames")
    parser.add_argument("--step", type=int, default=20, help="Save every N-th frame")
    parser.add_argument("--clean_start", action='store_true', help="Clear the output directory before starting")
    args = parser.parse_args()

    extract_frames(args.video, args.out, args.step, args.clean_start)
