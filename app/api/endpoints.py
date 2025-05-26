from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
import os
import shutil
from typing import List, Optional
import uuid
from app.services.process_image import process_image
from app.services.process_video import process_video
from app.services.process_pdf import process_pdf
from app.utils.file import validate_file, get_file_type
from app.core.config import UPLOAD_FOLDER, RESULTS_FOLDER

router = APIRouter()

# Đảm bảo thư mục upload tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get("/health")
async def health_check():
    """
    Endpoint kiểm tra trạng thái API
    """
    return {"status": "ok", "message": "API is running"}

@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    """
    Endpoint để upload file (ảnh, video, PDF) và phát hiện 'đường lưỡi bò'
    """
    # Tạo tên file duy nhất
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    # Kiểm tra định dạng file
    file_type = get_file_type(file.filename)
    if not file_type:
        raise HTTPException(status_code=400, detail="Định dạng file không được hỗ trợ. Vui lòng upload ảnh (JPG, PNG), video (MP4, AVI) hoặc PDF.")
    
    # Lưu file tạm thời
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file: {str(e)}")
    
    # Xử lý file dựa trên loại
    try:
        if file_type == "image":
            result = process_image(file_path)
        elif file_type == "video":
            result = process_video(file_path)
        elif file_type == "pdf":
            result = process_pdf(file_path)
        else:
            # Xóa file nếu không được hỗ trợ
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="Định dạng file không được hỗ trợ")
        
        # Chuyển đổi đường dẫn file thành URL có thể truy cập
        base_url = str(request.base_url).rstrip('/')
        
        if file_type == "image" and result.get("result_image"):
            # Lấy tên file từ đường dẫn đầy đủ
            result_filename = os.path.basename(result["result_image"])
            # Tạo URL cho hình ảnh kết quả
            result["result_image_url"] = f"{base_url}/results/{result_filename}"
        
        elif file_type == "video" and result.get("detections"):
            # Xử lý các frame đã phát hiện
            for detection in result["detections"]:
                if detection.get("frame_path"):
                    frame_filename = os.path.basename(detection["frame_path"])
                    detection["frame_url"] = f"{base_url}/results/{frame_filename}"
        
        elif file_type == "pdf" and result.get("detections"):
            # Xử lý các trang PDF đã phát hiện
            for detection in result["detections"]:
                if detection.get("page_path"):
                    page_filename = os.path.basename(detection["page_path"])
                    detection["page_url"] = f"{base_url}/results/{page_filename}"
        
        return JSONResponse(content=result)
    except Exception as e:
        # Xóa file nếu xử lý gặp lỗi
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý file: {str(e)}")
        
@router.get("/statistics")
async def get_statistics():
    """
    Endpoint để lấy thống kê về số lượng các loại file đã được xử lý
    """
    # Đếm số lượng các loại file đã được xử lý
    image_count = len([f for f in os.listdir(RESULTS_FOLDER) if f.endswith(tuple(('.jpg', '.jpeg', '.png'))) and not f.startswith('frame_') and not f.startswith('pdf_page_')])
    video_frame_count = len([f for f in os.listdir(RESULTS_FOLDER) if f.startswith('frame_')])
    pdf_page_count = len([f for f in os.listdir(RESULTS_FOLDER) if f.startswith('pdf_page_')])
    
    # Số lượng file có chứa "đường lưỡi bò" (đơn giản là đếm tất cả các file trong thư mục kết quả)
    total_detections = len(os.listdir(RESULTS_FOLDER))
    
    return {
        "total_processed": {
            "images": image_count,
            "video_frames": video_frame_count,
            "pdf_pages": pdf_page_count
        },
        "total_detections": total_detections
    }
