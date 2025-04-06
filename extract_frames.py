import cv2
import os
import argparse
from tqdm import tqdm

def extract_frames(video_path, output_dir, step=10, format='jpg'):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count, saved_count = 0, 0

    with tqdm(total=total_frames, desc="Extracting frames", unit="frame") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % step == 0:
                filename = os.path.join(output_dir, f"frame_{saved_count:04d}.{format}")
                if not cv2.imwrite(filename, frame):
                    raise IOError(f"Failed to write frame to {filename}")
                saved_count += 1
            frame_count += 1
            pbar.update(1)
    
    cap.release()
    print(f"✅ Extracted {saved_count} frames to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Path to input video")
    parser.add_argument("--out", default="images", help="Output directory")
    parser.add_argument("--step", type=int, default=10, help="Save every N-th frame")
    parser.add_argument("--format", default="jpg", help="Output image format (jpg, png, etc.)")
    args = parser.parse_args()

    extract_frames(args.video, args.out, args.step, args.format)
