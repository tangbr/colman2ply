import subprocess
import argparse
import os

def run_colmap(image_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # 1. Feature extraction
    subprocess.run([
        "colmap", "feature_extractor",
        "--database_path", os.path.join(output_dir, "database.db"),
        "--image_path", image_dir,
        "--ImageReader.single_camera", "1"
    ], check=True)

    # 2. Exhaustive matching
    subprocess.run([
        "colmap", "exhaustive_matcher",
        "--database_path", os.path.join(output_dir, "database.db")
    ], check=True)

    # 3. Sparse reconstruction
    sparse_dir = os.path.join(output_dir, "sparse")
    os.makedirs(sparse_dir, exist_ok=True)
    subprocess.run([
        "colmap", "mapper",
        "--database_path", os.path.join(output_dir, "database.db"),
        "--image_path", image_dir,
        "--output_path", sparse_dir
    ], check=True)

    print(f"✅ COLMAP Sparse Reconstruction done at {sparse_dir}")

    # Optional: Convert model to text format (.ply)
    subprocess.run([
        "colmap", "model_converter",
        "--input_path", os.path.join(sparse_dir, "0"),
        "--output_path", os.path.join(output_dir, "model.ply"),
        "--output_type", "PLY"
    ], check=True)

    print(f"✅ PLY model created at {os.path.join(output_dir, 'model.ply')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", default="./images", help="Directory containing extracted images")
    parser.add_argument("--out", default="./output", help="Directory for COLMAP outputs")
    args = parser.parse_args()

    run_colmap(args.images, args.out)

