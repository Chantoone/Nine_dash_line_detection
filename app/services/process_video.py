import cv2
import os
import tempfile
import numpy as np
from app.core.model import get_detector
from app.utils.visual import draw_bounding_boxes
from app.core.config import VIDEO_FRAME_RATE, RESULTS_FOLDER

def process_video(video_path):
    """
    Xử lý video và phát hiện 'đường lưỡi bò' trong các frame
    
    Args:
        video_path (str): Đường dẫn đến file video
        
    Returns:
        dict: Kết quả phát hiện
    """
    # Tải mô hình
    detector = get_detector()
    
    # Mở video
    cap = cv2.VideoCapture(video_path)
    
    # Kiểm tra xem video có mở thành công không
    if not cap.isOpened():
        raise Exception(f"Không thể mở video: {video_path}")
    
    # Lấy thông tin video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Khoảng cách giữa các frame cần trích xuất (số frame giữa mỗi lần lấy mẫu)
    frame_step = int(fps / VIDEO_FRAME_RATE)
    if frame_step < 1:
        frame_step = 1
    
    # Khởi tạo kết quả
    result = {
        "detected": False,
        "detections": [],
        "detected_frames": []
    }
    
    # Tạo thư mục tạm để lưu các frame
    temp_dir = tempfile.mkdtemp()
    
    try:
        current_frame = 0
        while True:
            # Đọc frame
            ret, frame = cap.read()
            
            # Kiểm tra nếu đã đọc hết video
            if not ret:
                break
            
            # Chỉ xử lý các frame theo khoảng frame_step
            if current_frame % frame_step == 0:
                # Lưu frame thành ảnh tạm thời
                frame_path = os.path.join(temp_dir, f"frame_{current_frame}.jpg")
                cv2.imwrite(frame_path, frame)
                
                # Phát hiện đối tượng trong frame
                frame_result = detector.detect(frame_path)
                
                # Nếu phát hiện trong frame này
                if frame_result["detected"]:
                    result["detected"] = True
                    
                    # Vẽ bounding box lên frame
                    frame_output_path = os.path.join(RESULTS_FOLDER, f"frame_{current_frame}.jpg")
                    frame_result_path = draw_bounding_boxes(
                        frame_path, 
                        frame_result["detections"], 
                        frame_output_path
                    )
                    
                    # Thêm thông tin frame vào kết quả
                    result["detected_frames"].append({
                        "frame_number": current_frame,
                        "time": current_frame / fps,
                        "detections": frame_result["detections"],
                        "frame_path": frame_result_path
                    })
                
                # Xóa file ảnh tạm thời
                os.remove(frame_path)
            
            # Tăng số frame
            current_frame += 1
        
        # Trả về kết quả
        return {
            "result": result["detected"],
            "message": "Có đường lưỡi bò" if result["detected"] else "Không có đường lưỡi bò",
            "detections": result["detected_frames"]
        }
    
    finally:
        # Đóng video
        cap.release()
        
        # Xóa thư mục tạm
        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except:
            pass
