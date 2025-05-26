from app.core.model import get_detector
from app.utils.visual import draw_bounding_boxes
import os
from app.core.config import RESULTS_FOLDER

def process_image(image_path):
    """
    Xử lý và phát hiện 'đường lưỡi bò' trong file ảnh
    
    Args:
        image_path (str): Đường dẫn đến file ảnh
        
    Returns:
        dict: Kết quả phát hiện
    """
    # Tải mô hình
    detector = get_detector()
    
    # Phát hiện đối tượng trong ảnh
    result = detector.detect(image_path)
    
    # Nếu có phát hiện, vẽ bounding box và lưu ảnh kết quả
    if result["detected"]:
        # Tạo tên file kết quả
        base_name = os.path.basename(image_path)
        result_image_path = os.path.join(RESULTS_FOLDER, f"result_{base_name}")
        
        # Vẽ bounding box và lưu ảnh kết quả
        result_image_path = draw_bounding_boxes(
            image_path, 
            result["detections"], 
            result_image_path
        )
        
        # Thêm đường dẫn ảnh kết quả vào kết quả trả về
        result["result_image"] = result_image_path
    
    # Trả về kết quả
    return {
        "result": result["detected"],
        "message": "Có đường lưỡi bò" if result["detected"] else "Không có đường lưỡi bò",
        "detections": result["detections"],
        "result_image": result.get("result_image", None)
    }
