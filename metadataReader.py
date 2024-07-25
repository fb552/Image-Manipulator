import os
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import ffmpeg

def print_image_metadata(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        image.close()

        if exif_data:
            print(f"\nMetadata for {image_path}:")
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                print(f"{tag_name}: {value}")
        else:
            print(f"No EXIF data found for {image_path}")
    except Exception as e:
        print(f"Error retrieving EXIF data from {image_path}: {e}")

def print_video_metadata(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        print(f"\nMetadata for {video_path}:")
        for stream in probe['streams']:
            for key, value in stream.items():
                print(f"{key}: {value}")
        for key, value in probe['format'].items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Error retrieving metadata from {video_path}: {e}")

def process_files(directory):
    supported_formats = ['.jpg', '.jpeg', '.mp4', '.mov', '.avi']

    for filename in os.listdir(directory):
        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension in supported_formats:
            file_path = os.path.join(directory, filename)

            if file_extension in ['.jpg', '.jpeg']:
                print_image_metadata(file_path)
            elif file_extension in ['.mp4', '.mov', '.avi']:
                print_video_metadata(file_path)
            else:
                print(f"Unsupported file format: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print metadata for image and video files.")
    parser.add_argument("folder", help="Path to the folder containing the files.")
    args = parser.parse_args()

    process_files(args.folder)
