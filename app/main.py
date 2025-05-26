from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api import endpoints
from app.core.config import RESULTS_FOLDER, UPLOAD_FOLDER

app = FastAPI(title="Nine-dash Line Detection API")

# Cấu hình CORS để frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường sản phẩm, nên giới hạn origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đảm bảo thư mục kết quả tồn tại
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount thư mục kết quả để có thể truy cập các ảnh kết quả
app.mount("/results", StaticFiles(directory=RESULTS_FOLDER), name="results")

# Đăng ký các routes
app.include_router(endpoints.router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
