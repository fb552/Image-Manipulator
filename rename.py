import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_time(image_path):

    image = Image.open(image_path)
    exif_data = image._getexif()
    image.close()

    if exif_data:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)

            if tag_name == 'DateTimeOriginal':
                return value

        print(f"No creation date found for {image_path}")
        return None
    else:
        print(f"No metadata found for {image_path}")
        return None

def rename_images(directory):

    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            file_path = os.path.join(directory, filename)
            time = get_time(file_path)

            if time:
                # Convert creation time to desired format
                creation_time = datetime.strptime(time, '%Y:%m:%d %H:%M:%S')
                new_filename = creation_time.strftime('%Y%m%d_%H%M%S') + '.JPG'
                new_file_path = os.path.join(directory, new_filename)
                
                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed {filename} to {new_filename}")

folder_path = '/home/francesco/Desktop/test/'  # Insert path of folder with images
rename_images(folder_path)
