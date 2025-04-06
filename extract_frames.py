import cv2
import os
import argparse
from tqdm import tqdm
import shutil

def safe_directory_clear(directory):
    """Attempt to clear all contents of a directory safely, including feature data."""
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)  # Recreate the directory after clearing
    except Exception as e:
        print(f"Error: Failed to clear directory {directory} - {e}")

def delete_feature_data(feature_directory):
    """Deletes feature files to ensure no data is skipped due to pre-existing files."""
    try:
        for filename in os.listdir(feature_directory):
            file_path = os.path.join(feature_directory, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print(f"All feature data in {feature_directory} has been deleted.")
    except Exception as e:
        print(f"Error: Failed to delete feature data - {e}")

def assess_reconstruction_quality():
    # Placeholder for actual quality assessment logic
    return False

def extract_frames(video_path, output_dir, step=10, clean_start=False):
    if clean_start:
        safe_directory_clear(output_dir)
        # Optionally clear feature data directory if needed
        delete_feature_data(output_dir)

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

    # Optionally adjust frame step based on quality
    if assess_reconstruction_quality():
        args.step = max(10, args.step - 10)
    else:
        args.step = min(50, args.step + 10)

    extract_frames(args.video, args.out, args.step, args.clean_start)
