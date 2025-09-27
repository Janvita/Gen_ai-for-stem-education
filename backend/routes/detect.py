from fastapi import APIRouter, File, UploadFile
import cv2
import numpy as np
import easyocr
import re

router = APIRouter()
reader = easyocr.Reader(['en'])

reader = easyocr.Reader(['en'])

def detect_circles_with_text_from_image_bytes(image_bytes):
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            print("Failed to decode image")
            return []
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=20,
            param1=50,
            param2=100,
            minRadius=50,
            maxRadius=100
        )

        results = []
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            
            for i, (x, y, r) in enumerate(circles):
                # Crop region around circle
                top = max(y - r - 20, 0)
                bottom = min(y + r + 20, img.shape[0])
                left = max(x - r - 20, 0)
                right = min(x + r + 20, img.shape[1])
                crop = img[top:bottom, left:right]

                try:
                    ocr_result = reader.readtext(crop)
                    texts = [res[1].strip() for res in ocr_result]  
                except Exception as e:
                    print(f"OCR error for circle {i}: {e}")
                    texts = []

                # Parse into page_number + circle_text
                page_number, circle_text = "", ""
                for t in texts:
                    t_clean = t.strip()
                    
                    if re.match(r"^a\d+\.\d+$", t_clean, re.IGNORECASE):
                        page_number = t_clean
                    
                    elif re.match(r"^\d+$", t_clean):
                        circle_text = t_clean


                

                results.append({
                    "id": i + 1,
                    "x": int(x),
                    "y": int(y),
                    "r": int(r),
                    "page_number": page_number,
                    "circle_text": circle_text,
                    "raw_texts": texts 
                })

        return results
    
    except Exception as e:
        print(f"Circle detection error: {e}")
        return []



def detect_text_from_image_bytes(image_bytes):
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            print("Failed to decode image for text detection")
            return []

        results = reader.readtext(img)
        text_boxes = []

        for i, (bbox, text, confidence) in enumerate(results):
            if "'" in text or '"' in text:
                continue 

            if any(char.isdigit() for char in text):
                continue
         
            try:
                    x_coords = [point[0] for point in bbox]
                    y_coords = [point[1] for point in bbox]
                    
                    x1, x2 = int(min(x_coords)), int(max(x_coords))
                    y1, y2 = int(min(y_coords)), int(max(y_coords))

                    text_boxes.append({
                        "id": i + 1,
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                        "text": text.strip()
                    })
            except Exception as e:
                    print(f"Error processing text box {i}: {e}")
                    continue

        return text_boxes
    
    except Exception as e:
        print(f"Text detection error: {e}")
        return []


@router.post("/")
async def detect_circles(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()    
        circles_with_text = detect_circles_with_text_from_image_bytes(image_bytes)
        texts = detect_text_from_image_bytes(image_bytes)
        
        return {"circles": circles_with_text, "texts": texts}
    
    except Exception as e:
        print(f"Detection endpoint error: {e}")
        return {"error": str(e), "circles": [], "texts": []}