import os
import shutil
import difflib
from tqdm import tqdm
import argparse
from convertToMp4 import process_videos


source_dir = r"C:\Users\RENMA\Downloads\Main Setlist"  # Carpeta con videos
target_dir = r"E:\Songs\GH3\Quickplay"  # Carpeta destino de los videos


# Configurar el análisis de argumentos
parser = argparse.ArgumentParser(description='Transfiere videos entre carpetas con opciones de reemplazo y transferencia.')
parser.add_argument('-r', '--replace', action='store_true', help='Reemplaza el video si ya existe en el destino')
parser.add_argument('-m', '--move', action='store_true', help='Mueve el video en lugar de copiarlo. Por defecto, se copia.')
parser.add_argument('-t', '--threads', type=int, default=4, help='Máximo valor para paralelizar la conversión de video. (valor por defecto: 4)')


# Parsear los argumentos de línea de comandos
args = parser.parse_args()

def normalize_name(name):
    for char in ["'", " ", "-", "_", "&"]:
        name = name.replace(char, "").lower()
    return name

def find_best_match(source_name, target_names):
    normalized_source = normalize_name(source_name)
    matches = difflib.get_close_matches(normalized_source, target_names, n=1, cutoff=0.6)
    return matches[0] if matches else None

def transfer_videos(source_dir, target_dir, replace_existing=False, move=False):
    target_folders = {normalize_name(name): name for name in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, name))}
    
    source_folders = [folder for folder in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, folder))]
    
    for folder_name in tqdm(source_folders, desc="Transfiriendo videos"):
        match = find_best_match(folder_name.split(" - ")[-1], target_folders.keys())
        if match:
            source_video_path = os.path.join(source_dir, folder_name, "video.mp4")
            target_video_path = os.path.join(target_dir, target_folders[match], "video.mp4")
            
            # Comprobar si el video ya existe en el destino
            if not os.path.exists(target_video_path) or replace_existing:
                if os.path.exists(source_video_path):
                    if move:
                        shutil.move(source_video_path, target_video_path)
                    else:
                        shutil.copy(source_video_path, target_video_path)
                else:
                    print(f"No se encontró 'video.mp4' en {os.path.join(source_dir, folder_name)}")
            else:
                print(f"'video.mp4' ya existe en {os.path.join(target_dir, target_folders[match])} y no será movido.")
        else:
            print(f"No se encontró una coincidencia para '{folder_name}'")




if __name__ == '__main__':
    print("Converting videos from webm to mp4...")
    process_videos(source_dir, max_threads=args.threads)
    print("Transfiriendo videos...")
    transfer_videos(source_dir, target_dir, replace_existing=args.replace, move=args.move)