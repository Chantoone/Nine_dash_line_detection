import os
from pathlib import Path

# Thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_PATH = os.path.join(BASE_DIR, "model", "faster-rcnn_vgg_v2.pth")
MODEL_50_PATH= os.path.join(BASE_DIR, "model", "faster_rcnn_resnet_50_weights_v2.pth")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

RESULTS_FOLDER = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_FOLDER, exist_ok=True)

CONFIDENCE_THRESHOLD = 0.7

ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
ALLOWED_VIDEO_EXTENSIONS = [".mp4", ".avi"]
ALLOWED_PDF_EXTENSIONS = [".pdf"]

VIDEO_FRAME_RATE = 2
