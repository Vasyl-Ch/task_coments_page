from celery import shared_task
from PIL import Image
import os


@shared_task
def resize_image(file_path: str, max_size: tuple[int, int] = (320, 240)):
    """
    Making picture smaller if picture bigger than 320х240
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    try:
        with Image.open(file_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(file_path)

        return f"Resized: {file_path}"
    except Exception as e:
        return f"Error: {e}"
