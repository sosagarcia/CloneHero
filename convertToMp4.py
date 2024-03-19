# Importing required libraries
import os
import subprocess
from alive_progress import alive_bar

SOURCE_PATH = r"C:\Users\RENMA\Downloads\Main Setlist"  # Carpeta con videos

# Function to find all 'video.webm' files in a directory and its subdirectories
def find_webm_files(directory):
    webm_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "video.webm":
                webm_files.append(os.path.join(root, file))
    return webm_files

# Function to convert 'video.webm' to 'video.mp4' without audio using GPU acceleration
def convert_video(file_path):
    output_path = file_path.replace('.webm', '.mp4')
    # Command to use ffmpeg with GPU acceleration and no audio
    command = ['ffmpeg', '-y', '-i', file_path, '-c:v', 'h264_nvenc', '-preset', 'slow', '-cq', '28', '-an', output_path]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# Main function to process videos sequentially
def process_videos(directory):
    webm_files = find_webm_files(directory)
    total_files = len(webm_files)
    
    with alive_bar(total_files, title='Overall Conversion Progress', bar='smooth') as bar:
        for file in webm_files:
            folder_name = os.path.basename(os.path.dirname(file))
            print(f"Starting conversion of {folder_name}...")  
            convert_video(file)
            bar()

if __name__ == '__main__':
    print("Converting videos from webm to mp4...")
    process_videos(SOURCE_PATH)
