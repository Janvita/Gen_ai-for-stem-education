"""
region_detection.py

This module provides functionality to detect text inside a specific region 
of an uploaded image using OpenCV and EasyOCR.

Key functionalities:
- Extract a specified rectangular region from an image.
- Perform OCR (Optical Character Recognition) on the cropped region.
- Return detected text boxes along with their coordinates.
- Return the cropped region as a base64-encoded image.
"""

from fastapi import APIRouter, File, UploadFile, Form
import cv2
import numpy as np
import easyocr
import base64

# Initialize FastAPI router
router = APIRouter()

# Initialize EasyOCR reader (English language)
reader = easyocr.Reader(['en'])


def detect_text_in_region(img, region):
    """
    Detects text within a specified rectangular region of an image.

    Steps:
    1. Crop the region of interest (ROI) from the original image.
    2. Run EasyOCR to detect text inside the cropped region.
    3. Adjust bounding box coordinates relative to the original image.
    4. Convert the cropped region to base64 for return.

    Args:
        img (numpy.ndarray): The original OpenCV image.
        region (tuple): A tuple (x, y, w, h) specifying the top-left 
                        coordinates, width, and height of the region.

    Returns:
        tuple:
            - text_boxes (list of dict): Each dict contains:
                - id (int): Box index
                - x1, y1 (int): Top-left coordinates
                - x2, y2 (int): Bottom-right coordinates
                - text (str): Detected text
            - crop_base64 (str): Base64-encoded cropped image.
    """
    x, y, w, h = region
    crop = img[y:y+h, x:x+w]
    results = reader.readtext(crop)
    text_boxes = []

    for i, (bbox, text, prob) in enumerate(results):
        (top_left, _, bottom_right, _) = bbox
        top_left = [int(top_left[0] + x), int(top_left[1] + y)]
        bottom_right = [int(bottom_right[0] + x), int(bottom_right[1] + y)]
        text_boxes.append({
            "id": i+1,
            "x1": top_left[0],
            "y1": top_left[1],
            "x2": bottom_right[0],
            "y2": bottom_right[1],
            "text": text
        })

    # Convert cropped region to base64 string
    _, buffer = cv2.imencode(".jpg", crop)
    crop_base64 = base64.b64encode(buffer).decode("utf-8")

    return text_boxes, crop_base64


@router.post("/region-detect")
async def detect_in_region(
    file: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    w: int = Form(...),
    h: int = Form(...)
):
    """
    FastAPI endpoint to detect text within a user-specified region of an uploaded image.

    Steps:
    1. Accepts an image file and region coordinates (x, y, w, h).
    2. Decodes the image into an OpenCV format.
    3. Calls `detect_text_in_region` to extract text and crop region.
    4. Returns:
        - Detected text boxes with coordinates and recognized text.
        - Cropped image region as a base64 string.

    
    """
    image_bytes = await file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detections, crop_base64 = detect_text_in_region(img, (x, y, w, h))
    return {
        "detections": detections,
        "cropped_image": f"data:image/jpeg;base64,{crop_base64}"
    }
