import os
from pathlib import Path

# Thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Đường dẫn đến mô hình
MODEL_PATH = os.path.join(BASE_DIR, "model", "faster_rcnn.pth")

# Thư mục lưu trữ file tạm thời
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Thư mục lưu trữ kết quả
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Ngưỡng tin cậy cho việc phát hiện
CONFIDENCE_THRESHOLD = 0.7

# Định dạng file được hỗ trợ
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
ALLOWED_VIDEO_EXTENSIONS = [".mp4", ".avi"]
ALLOWED_PDF_EXTENSIONS = [".pdf"]

# Số frame trích xuất từ video mỗi giây
VIDEO_FRAME_RATE = 1
