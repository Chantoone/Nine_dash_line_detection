import os
from pathlib import Path
from app.core.config import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
    ALLOWED_PDF_EXTENSIONS
)

def validate_file(filename):

    ext = os.path.splitext(filename)[1].lower()

    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return True
    if ext in ALLOWED_VIDEO_EXTENSIONS:
        return True
    if ext in ALLOWED_PDF_EXTENSIONS:
        return True
    
    return False

def get_file_type(filename):

    ext = os.path.splitext(filename)[1].lower()
    
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        return "image"
    if ext in ALLOWED_VIDEO_EXTENSIONS:
        return "video"
    if ext in ALLOWED_PDF_EXTENSIONS:
        return "pdf"
    
    return None

def save_result_image(original_image_path, result_data, output_path=None):

    from PIL import Image, ImageDraw
    import os

    if output_path is None:
        filename = os.path.basename(original_image_path)
        output_dir = os.path.join(os.path.dirname(original_image_path), "results")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"result_{filename}")

    image = Image.open(original_image_path)
    draw = ImageDraw.Draw(image)

    for detection in result_data["detections"]:
        box = detection["box"]
        confidence = detection["confidence"]

        draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline="red", width=3)

        text = f"Nine-dash line: {confidence:.2f}"
        draw.text((box[0], box[1] - 10), text, fill="red")

    image.save(output_path)
    return output_path
