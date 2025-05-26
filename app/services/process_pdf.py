import os
import tempfile
from pdf2image import convert_from_path
from app.core.model import get_detector
from app.utils.visual import draw_bounding_boxes
from app.core.config import RESULTS_FOLDER

def process_pdf(pdf_path):
    """
    Xử lý file PDF và phát hiện 'đường lưỡi bò' trong các trang
    
    Args:
        pdf_path (str): Đường dẫn đến file PDF
        
    Returns:
        dict: Kết quả phát hiện
    """
    # Tải mô hình
    detector = get_detector()
    
    # Khởi tạo kết quả
    result = {
        "detected": False,
        "detections": []
    }
    
    # Tạo thư mục tạm để lưu các ảnh từ PDF
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Chuyển đổi các trang PDF thành ảnh
        pages = convert_from_path(pdf_path)
        
        for i, page in enumerate(pages):
            # Lưu trang thành ảnh tạm thời
            page_path = os.path.join(temp_dir, f"page_{i + 1}.jpg")
            page.save(page_path, "JPEG")
            
            # Phát hiện đối tượng trong trang
            page_result = detector.detect(page_path)
            
            # Nếu phát hiện trong trang này
            if page_result["detected"]:
                result["detected"] = True
                
                # Vẽ bounding box lên trang
                page_output_path = os.path.join(RESULTS_FOLDER, f"pdf_page_{i + 1}.jpg")
                page_result_path = draw_bounding_boxes(
                    page_path, 
                    page_result["detections"], 
                    page_output_path
                )
                
                # Thêm thông tin trang vào kết quả
                result["detections"].append({
                    "page_number": i + 1,
                    "detections": page_result["detections"],
                    "page_path": page_result_path
                })
            
            # Xóa file ảnh tạm thời
            os.remove(page_path)
        
        # Trả về kết quả
        return {
            "result": result["detected"],
            "message": "Có đường lưỡi bò" if result["detected"] else "Không có đường lưỡi bò",
            "detections": result["detections"]
        }
    
    finally:
        # Xóa thư mục tạm
        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except:
            pass
