import cv2
import os
import tempfile
import numpy as np
from app.core.model import get_detector
from app.utils.visual import draw_bounding_boxes
from app.core.config import VIDEO_FRAME_RATE, RESULTS_FOLDER

def process_video(video_path):

    detector = get_detector()

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception(f"Không thể mở video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_step = int(fps / VIDEO_FRAME_RATE)
    if frame_step < 1:
        frame_step = 1

    result = {
        "detected": False,
        "detections": [],
        "detected_frames": []
    }

    temp_dir = tempfile.mkdtemp()
    
    try:
        current_frame = 0
        while True:

            ret, frame = cap.read()

            if not ret:
                break

            if current_frame % frame_step == 0:
                frame_path = os.path.join(temp_dir, f"frame_{current_frame}.jpg")
                cv2.imwrite(frame_path, frame)

                frame_result = detector.detect(frame_path)

                if frame_result["detected"]:
                    result["detected"] = True

                    frame_output_path = os.path.join(RESULTS_FOLDER, f"frame_{current_frame}.jpg")
                    frame_result_path = draw_bounding_boxes(
                        frame_path, 
                        frame_result["detections"], 
                        frame_output_path
                    )

                    result["detected_frames"].append({
                        "frame_number": current_frame,
                        "time": current_frame / fps,
                        "detections": frame_result["detections"],
                        "frame_path": frame_result_path
                    })

                os.remove(frame_path)

            current_frame += 1

        return {
            "result": result["detected"],
            "message": "Có đường lưỡi bò" if result["detected"] else "Không có đường lưỡi bò",
            "detections": result["detected_frames"]
        }
    
    finally:

        cap.release()

        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except:
            pass
