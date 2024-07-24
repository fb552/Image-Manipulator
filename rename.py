import os
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import ffmpeg

def get_image_time(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        image.close()

        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)

                if tag_name == 'DateTimeOriginal':
                    return value
                elif tag_name == 'DateTime':
                    return value
    except Exception as e:
        print(f"Error retrieving EXIF data from {image_path}: {e}")
    
def get_video_time(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        creation_time = probe['format']['tags'].get('creation_time', None)

        if creation_time:
            return datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        
    except Exception as e:
        print(f"Error retrieving creation time from {video_path}: {e}")
    return None

def rename_files(directory):
    supported_formats = ['.jpg', '.jpeg', '.mp4', '.mov', '.avi']

    for filename in os.listdir(directory):
        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension in supported_formats:
            file_path = os.path.join(directory, filename)
            creation_time = None

            if file_extension in ['.jpg', '.jpeg']:
                creation_time = get_image_time(file_path)
                
            elif file_extension in ['.mp4', '.mov']:
                creation_time = get_video_time(file_path)

            if creation_time:
                # Convert creation time to suitable format
                if isinstance(creation_time, str):
                    time = datetime.strptime(creation_time, '%Y:%m:%d %H:%M:%S')
                else:
                    time = creation_time

                new_filename = time.strftime('%Y%m%d_%H%M%S') + file_extension.upper()
                new_file_path = os.path.join(directory, new_filename)
                
                # Rename the file wile ignoring those already renamed
                if not os.path.exists(new_file_path):
                    os.rename(file_path, new_file_path)
                    print(f'Renamed {filename} to {new_filename}')
                else:
                    print(f'File {new_filename} already exists, skipping {filename}')
            else:
                print(f'No creation time found for {filename}, skipping')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename image and video files based on their creation timestamps.")
    parser.add_argument("folder", help="Path to the folder containing the files to rename.")
    args = parser.parse_args()

    rename_files(args.folder)
