import subprocess
import argparse
import os
import matplotlib.pyplot as plt

def run_command(command):
    output = []
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Output:", result.stdout)
        output = result.stdout.splitlines()
        return output, True
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}\n{e.stderr}")
        return output, False

def initialize_database(database_path):
    return run_command([
        "colmap", "database_creator",
        "--database_path", database_path
    ])[1]

def plot_metrics(metrics, title, ylabel):
    iterations = range(1, len(metrics) + 1)
    plt.figure()
    plt.plot(iterations, metrics, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel('Iteration')
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def extract_metrics_from_output(output):
    costs = []
    gradients = []
    for line in output.split('\n'):
        parts = line.strip().split()
        if len(parts) > 1 and parts[0].isdigit():  # Checking if the line starts with an iteration number
            try:
                cost = float(parts[1])  # Assuming 'cost' is the second element
                gradient = float(parts[3])  # Assuming 'gradient' is the fourth element
                costs.append(cost)
                gradients.append(gradient)
            except ValueError as e:
                print(f"Warning: Could not convert values to float. Error: {str(e)}")
    return costs, gradients

def run_colmap(image_dir, output_dir, verbose=False):
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
        feature_extraction_command.append("--verbose")

    run_command(feature_extraction_command)

    # Exhaustive matching
    run_command([
        "colmap", "exhaustive_matcher",
        "--database_path", database_path,
        "--SiftMatching.use_gpu", "0"
    ])

    # Sparse reconstruction
    sparse_dir = os.path.join(output_dir, "sparse")
    os.makedirs(sparse_dir, exist_ok=True)
    output, success = run_command([
        "colmap", "mapper",
        "--database_path", database_path,
        "--image_path", image_dir,
        "--output_path", sparse_dir
    ])
    if not success:
        print("Failed to execute sparse reconstruction.")
        return

    print(f"✅ COLMAP Sparse Reconstruction done at {sparse_dir}")

    # Convert model to text format (.ply)
    run_command([
        "colmap", "model_converter",
        "--input_path", os.path.join(sparse_dir, "0"),
        "--output_path", os.path.join(output_dir, "model.ply"),
        "--output_type", "PLY"
    ])

    costs, gradients = extract_metrics_from_output(output)
    plot_metrics(costs, 'Cost Over Iterations', 'Cost')
    plot_metrics(gradients, 'Gradient Over Iterations', 'Gradient')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", default="./images", help="Directory containing extracted images")
    parser.add_argument("--out", default="./output", help="Directory for COLMAP outputs")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    run_colmap(args.images, args.out, args.verbose)
