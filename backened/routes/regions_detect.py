from fastapi import APIRouter, File, UploadFile, Form
import cv2
import numpy as np
import easyocr
import base64

router = APIRouter()
reader = easyocr.Reader(['en'])

def detect_text_in_region(img, region):
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
    image_bytes = await file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detections, crop_base64 = detect_text_in_region(img, (x, y, w, h))
    return {
        "detections": detections,
        "cropped_image": f"data:image/jpeg;base64,{crop_base64}"
    }
