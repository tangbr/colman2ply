import cv2
import os
import argparse
from tqdm import tqdm
import shutil
import logging
import numpy as np

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def safe_directory_clear(directory):
    """Safely clears all contents of a directory, recreating it afterwards."""
    try:
        shutil.rmtree(directory)
        os.makedirs(directory)
        logging.info(f"Directory {directory} cleared and recreated.")
    except Exception as e:
        logging.error(f"Failed to clear directory {directory}: {e}")
        raise

def extract_frames(video_path, output_dir, step=10, clean_start=False):
    """Extracts frames from a video file at a given step interval."""
    if clean_start:
        safe_directory_clear(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(f"Cannot open video: {video_path}")
        raise IOError(f"Cannot open video: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    saved_count = 0

    try:
        with tqdm(total=total_frames) as pbar:
            frame_count = 0
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
    finally:
        cap.release()
        logging.info(f"Extracted {saved_count} frames to {output_dir}")

def assess_reconstruction_quality(feature_data_file):
    """Assess the quality of reconstruction based on the average number of features per frame."""
    try:
        with open(feature_data_file, 'r') as file:
            feature_counts = [int(line.strip()) for line in file.readlines()]

        average_features = np.mean(feature_counts)
        quality_threshold = 1000  # Example threshold

        return average_features > quality_threshold
    except Exception as e:
        logging.error(f"Error reading feature data or assessing quality: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Path to the input video file")
    parser.add_argument("--out", default="images", help="Output directory for extracted frames")
    parser.add_argument("--step", type=int, default=20, help="Interval of frames to extract")
    parser.add_argument("--clean_start", action='store_true', help="Clear the output directory before starting")
    parser.add_argument("--feature_data_file", help="Path to the feature data file for assessing quality (optional)")

    args = parser.parse_args()

    # Determine the path to the feature data file based on input or by generating it dynamically
    if not args.feature_data_file:
        base_dir = "/app/data"  # Assuming this is your desired default location
        feature_data_filename = os.path.basename(args.video).replace('.mp4', '_features.json')
        feature_data_file_path = os.path.join(base_dir, feature_data_filename)
    else:
        feature_data_file_path = args.feature_data_file

    print("Feature Data File Path:", feature_data_file_path)  # For verification

    # Check the quality and adjust frame step accordingly
    if assess_reconstruction_quality(feature_data_file_path):
        args.step = max(10, args.step - 10)
    else:
        args.step = min(50, args.step + 10)

    extract_frames(args.video, args.out, args.step, args.clean_start)
