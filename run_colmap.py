import subprocess
import argparse
import os

def initialize_database(database_path):
    return run_command([
        "colmap", "database_creator",
        "--database_path", database_path
    ])

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)  # Optionally print or log the output
        return True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}\n{e.stderr}")
        return False

def run_colmap(image_dir, output_dir, use_gpu=False, verbose=False):
    os.makedirs(output_dir, exist_ok=True)
    database_path = os.path.join(output_dir, "database.db")

    # Initialize database
    if not initialize_database(database_path):
        print("Database initialization failed.")
        return

    # Feature extraction
    feature_extraction_command = [
        "colmap", "feature_extractor",
        "--database_path", database_path,
        "--image_path", image_dir,
        "--ImageReader.single_camera", "1",
        "--SiftExtraction.use_gpu", "0"
    ]

    if verbose:
        feature_extraction_command.append("--log_level", "1")  # Use a lower log level for less verbose output

    if not run_command(feature_extraction_command):
        print("Failed to execute feature extraction.")
        return

    # Exhaustive matching
    matching_command = [
        "colmap", "exhaustive_matcher",
        "--database_path", database_path,
        "--SiftMatching.use_gpu", "0"
    ]

    if not run_command(matching_command):
        print("Failed to execute exhaustive matching.")
        return

    # Sparse reconstruction
    sparse_dir = os.path.join(output_dir, "sparse")
    os.makedirs(sparse_dir, exist_ok=True)
    if not run_command([
        "colmap", "mapper",
        "--database_path", database_path,
        "--image_path", image_dir,
        "--output_path", sparse_dir
    ]):
        print("Failed to execute sparse reconstruction.")
        return

    print(f"✅ COLMAP Sparse Reconstruction done at {sparse_dir}")

    # Convert model to text format (.ply)
    if not run_command([
        "colmap", "model_converter",
        "--input_path", os.path.join(sparse_dir, "0"),
        "--output_path", os.path.join(output_dir, "model.ply"),
        "--output_type", "PLY"
    ]):
        print("Failed to convert model to PLY.")
        return

    print(f"✅ PLY model created at {os.path.join(output_dir, 'model.ply')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", default="./images", help="Directory containing extracted images")
    parser.add_argument("--out", default="./output", help="Directory for COLMAP outputs")
    parser.add_argument("--use_gpu", action="store_true", help="Use GPU for processing (if available)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    run_colmap(args.images, args.out, args.use_gpu, args.verbose)
