import os
import subprocess

def delete_files(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def main():
    print('Cleaning start...')
    delete_files('/app/images')
    delete_files('/app/output')

    print('Files in /app/images after deletion:')
    os.system('ls -alh /app/images')

    print('Files in /app/output after deletion:')
    os.system('ls -alh /app/output')

    print('Starting frame extraction...')
    subprocess.run(['xvfb-run', '--auto-servernum', '--server-args=-screen 0 1024x768x24', 'python3', 'extract_frames.py', '--video', '/app/data/my_video.mp4', '--out', '/app/images'])

    print('Starting COLMAP...')
    subprocess.run(['python3', 'run_colmap.py', '--images', '/app/images', '--out', '/app/output'])

    print('Starting transformation to Gaussian splatting...')
    subprocess.run(['python3', 'trans_to_gaussian_splatt.py', '--input', '/app/output/model.ply', '--output', '/app/output/processed.ply'])

if __name__ == "__main__":
    main()
