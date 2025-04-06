import subprocess
import argparse
import os

def initialize_database(database_path):
    return run_command(["colmap", "database_creator", "--database_path", database_path])

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)  # Print the standard output for diagnostics
        return True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}\n{e.stderr}")  # Print detailed error info
        return False

def run_colmap(image_dir, output_dir, verbose=False):
    os.makedirs(output_dir, exist_ok=True)
    database_path = os.path.join(output_dir, "database.db")

    # Initialize database
    if not initialize_database(database_path):
        print("Database initialization failed.")
        return

    # Feature extraction
    if not run_command([
        "colmap", "feature_extractor",
        "--database_path", database_path,
        "--image_path", image_dir,
        "--ImageReader.single_camera", "1",
        "--SiftExtraction.use_gpu", "0",
        "--verbose" if verbose else "--quiet"
    ]):
        print("Failed to execute feature extraction.")
        return

    # Exhaustive matching
    if not run_command([
        "colmap", "exhaustive_matcher",
        "--database_path", database_path,
        "--SiftMatching.use_gpu", "0",
        "--verbose" if verbose else "--quiet"
    ]):
        print("Failed to execute exhaustive matching.")
        return

    # Sparse reconstruction
    if not run_command([
        "colmap", "mapper",
        "--database_path", database_path,
        "--image_path", image_dir,
        "--output_path", os.path.join(output_dir, "sparse"),
        "--Mapper.num_threads", "4",
        "--Mapper.init_min_tri_angle", "4",
        "--Mapper.min_num_matches", "50",
        "--verbose" if verbose else "--quiet"
    ]):
        print("Failed to execute sparse reconstruction.")
        return

    print("Sparse Reconstruction completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", default="./images", help="Directory containing extracted images")
    parser.add_argument("--out", default="./output", help="Directory for COLMAP outputs")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    run_colmap(args.images, args.out, args.verbose)
