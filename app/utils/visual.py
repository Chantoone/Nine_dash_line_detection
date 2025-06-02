from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from app.core.config import RESULTS_FOLDER

def draw_bounding_boxes(image_path, detections, output_path=None):

    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    for detection in detections:
        box = detection["box"]
        confidence = detection["confidence"]
        
        # Vẽ hộp giới hạn
        draw.rectangle(
            [(box[0], box[1]), (box[2], box[3])], 
            outline="green",
            width=8
        )
        label = f"Nine-dash line: {confidence:.2f}"
        left, top, right, bottom = draw.textbbox((0, 0), label, font=font)
        text_width = right - left
        text_height = bottom - top

        draw.rectangle(
            [(box[0], box[1] - text_height - 4), (box[0] + text_width, box[1])],
            fill="red"
        )
        
        # Vẽ văn bản
        draw.text(
            (box[0], box[1] - text_height - 2),
            label,
            fill="white",
            font=font
        )

    if output_path is None:
        base_name = os.path.basename(image_path)
        output_path = os.path.join(RESULTS_FOLDER, f"result_{base_name}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    image.save(output_path)
    
    return output_path
