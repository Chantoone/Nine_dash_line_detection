import os
import tempfile
import fitz  # PyMuPDF
from app.core.model import get_detector
from app.utils.visual import draw_bounding_boxes
from app.core.config import RESULTS_FOLDER

def process_pdf(pdf_path):

    detector = get_detector()

    result = {
        "detected": False,
        "detections": []
    }

    temp_dir = tempfile.mkdtemp()
    try:
        pdf_document = fitz.open(pdf_path)
        
        for i, page in enumerate(pdf_document):

            page_path = os.path.join(temp_dir, f"page_{i + 1}.jpg")

            pix = page.get_pixmap(dpi=300)
            pix.save(page_path)

            page_result = detector.detect(page_path)

            if page_result["detected"]:
                result["detected"] = True

                page_output_path = os.path.join(RESULTS_FOLDER, f"pdf_page_{i + 1}.jpg")
                page_result_path = draw_bounding_boxes(
                    page_path, 
                    page_result["detections"], 
                    page_output_path
                )

                result["detections"].append({
                    "page_number": i + 1,
                    "detections": page_result["detections"],
                    "page_path": page_result_path
                })

            os.remove(page_path)

        return {
            "result": result["detected"],
            "message": "Có đường lưỡi bò" if result["detected"] else "Không có đường lưỡi bò",
            "detections": result["detections"]
        }
    
    finally:
        try:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
        except:
            pass
