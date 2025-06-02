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

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    file_type = get_file_type(file.filename)
    if not file_type:
        raise HTTPException(status_code=400, detail="Định dạng file không được hỗ trợ. Vui lòng upload ảnh (JPG, PNG), video (MP4, AVI) hoặc PDF.")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file: {str(e)}")

    try:
        if file_type == "image":
            result = process_image(file_path)
        elif file_type == "video":
            result = process_video(file_path)
        elif file_type == "pdf":
            result = process_pdf(file_path)
        else:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail="Định dạng file không được hỗ trợ")

        base_url = str(request.base_url).rstrip('/')
        
        if file_type == "image" and result.get("result_image"):

            result_filename = os.path.basename(result["result_image"])

            result["result_image_url"] = f"{base_url}/results/{result_filename}"
        
        elif file_type == "video" and result.get("detections"):

            for detection in result["detections"]:
                if detection.get("frame_path"):
                    frame_filename = os.path.basename(detection["frame_path"])
                    detection["frame_url"] = f"{base_url}/results/{frame_filename}"
        
        elif file_type == "pdf" and result.get("detections"):

            for detection in result["detections"]:
                if detection.get("page_path"):
                    page_filename = os.path.basename(detection["page_path"])
                    detection["page_url"] = f"{base_url}/results/{page_filename}"
        
        return JSONResponse(content=result)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý file: {str(e)}")
        
