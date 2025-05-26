from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from app.core.config import RESULTS_FOLDER

def draw_bounding_boxes(image_path, detections, output_path=None):
    """
    Vẽ các bounding box trên ảnh và lưu ảnh kết quả
    
    Args:
        image_path (str): Đường dẫn đến ảnh gốc
        detections (list): Danh sách các phát hiện, mỗi phát hiện gồm:
            - box (list): Tọa độ của bounding box [x1, y1, x2, y2]
            - confidence (float): Độ tin cậy
        output_path (str, optional): Đường dẫn để lưu ảnh kết quả
            
    Returns:
        str: Đường dẫn đến ảnh kết quả
    """
    # Tải ảnh gốc
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    
    # Cố gắng tải font, nếu không có sẽ sử dụng font mặc định
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    # Vẽ các bounding box
    for detection in detections:
        box = detection["box"]
        confidence = detection["confidence"]
        
        # Vẽ hộp giới hạn
        draw.rectangle(
            [(box[0], box[1]), (box[2], box[3])], 
            outline="red", 
            width=3
        )
          # Vẽ nhãn với độ tin cậy
        label = f"Nine-dash line: {confidence:.2f}"
        # Thay textsize bằng textbbox trong phiên bản mới của Pillow
        left, top, right, bottom = draw.textbbox((0, 0), label, font=font)
        text_width = right - left
        text_height = bottom - top
        
        # Tạo một hình chữ nhật đỏ làm nền cho văn bản
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
    
    # Tạo tên file kết quả nếu không có đường dẫn đầu ra
    if output_path is None:
        base_name = os.path.basename(image_path)
        output_path = os.path.join(RESULTS_FOLDER, f"result_{base_name}")
    
    # Đảm bảo thư mục đích tồn tại
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Lưu ảnh kết quả
    image.save(output_path)
    
    return output_path
