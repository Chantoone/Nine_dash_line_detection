from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api import endpoints
from app.core.config import RESULTS_FOLDER, UPLOAD_FOLDER

app = FastAPI(title="Nine-dash Line Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.mount("/results", StaticFiles(directory=RESULTS_FOLDER), name="results")

app.include_router(endpoints.router)

