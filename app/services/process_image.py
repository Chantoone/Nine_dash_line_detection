from app.core.model import get_detector
from app.utils.visual import draw_bounding_boxes
import os
from app.core.config import RESULTS_FOLDER

def process_image(image_path):

    detector = get_detector()

    result = detector.detect(image_path)

    if result["detected"]:
        base_name = os.path.basename(image_path)
        result_image_path = os.path.join(RESULTS_FOLDER, f"result_{base_name}")

        result_image_path = draw_bounding_boxes(
            image_path, 
            result["detections"], 
            result_image_path
        )

        result["result_image"] = result_image_path

    return {
        "result": result["detected"],
        "message": "Có đường lưỡi bò" if result["detected"] else "Không có đường lưỡi bò",
        "detections": result["detections"],
        "result_image": result.get("result_image", None)
    }
