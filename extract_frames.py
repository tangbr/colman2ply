# extract_frames.py
import cv2
import os
import argparse
from tqdm import tqdm

def extract_frames(video_path, output_dir, step=1):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video {video_path}")

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    idx = 0
    saved = 0
    with tqdm(total=total) as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if idx % step == 0:
                filename = os.path.join(output_dir, f"frame_{saved:04d}.jpg")
                cv2.imwrite(filename, frame)
                saved += 1
            idx += 1
            pbar.update(1)
    cap.release()
    print(f"Extracted {saved} frames to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Path to input video")
    parser.add_argument("--out", default="images", help="Output directory")
    parser.add_argument("--step", type=int, default=50, help="Save every N-th frame")
    args = parser.parse_args()
    extract_frames(args.video, args.out, args.step)

