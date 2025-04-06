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
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

def assess_reconstruction_quality():
    """Assess the quality of the reconstruction based on hypothetical metrics."""
    num_matched_features = 500
    average_reprojection_error = 1.2
    low_feature_threshold = 800
    high_error_threshold = 1.0

    if num_matched_features < low_feature_threshold or average_reprojection_error > high_error_threshold:
        return True
    else:
        return False

def extract_frames(video_path, output_dir, step=10, clean_start=False):
    """Extract frames from a video at a specified step interval."""
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

    # Adjust frame step based on the assessed reconstruction quality
    if assess_reconstruction_quality():
        args.step = max(10, args.step - 10)  # Decrease step if quality is low to increase overlap
    else:
        args.step = min(50, args.step + 10)  # Increase step if computation needs reduction

    extract_frames(args.video, args.out, args.step, args.clean_start)
