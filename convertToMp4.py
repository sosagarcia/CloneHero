from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import os

def convert_video_to_mp4(video_path, output_path):
    """
    Converts a video from webm format to mp4 format using moviepy.
    """
    clip = VideoFileClip(str(video_path))
    clip.write_videofile(str(output_path), audio=False, logger=None)  # logger=None to suppress the printing
    clip.close()

def process_videos(folder_path, max_threads):
    """
    Searches for all webm files in the given folder and its subfolders,
    and converts them to mp4 format in parallel.
    """
    folder_path = Path(folder_path)
    webm_files = list(folder_path.rglob("*.webm"))  # List all webm files

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(convert_video_to_mp4, webm_file, webm_file.with_suffix('.mp4')): webm_file for webm_file in webm_files}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Converting Videos"):
            future.result()  # to raise exceptions if any

# Uncomment the following line to use the function with your specific folder path and max_threads
# process_videos("/path/to/your/folder", 4)
