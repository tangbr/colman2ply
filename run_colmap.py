import subprocess
import argparse
import os

def initialize_database(database_path):
    subprocess.run([
        "colmap", "database_creator",
        "--database_path", database_path
    ], check=True)

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return False
    return True

# Example usage within your existing functions
if not run_command([
    "colmap", "feature_extractor",
    "--database_path", os.path.join(output_dir, "database.db"),
    "--image_path", image_dir,
    "--ImageReader.single_camera", "1",
    "--SiftExtraction.use_gpu", "0",
    "--verbose"
]):
    print("Failed to execute feature extraction.")

    # 2. Exhaustive matching
    subprocess.run([
        "colmap", "exhaustive_matcher",
        "--database_path", os.path.join(output_dir, "database.db"),
        "--SiftMatching.use_gpu", "0"
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

