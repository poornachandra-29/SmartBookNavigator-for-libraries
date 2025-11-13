import os
import io
import cv2
import numpy as np
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend import BookDetector  


app = FastAPI()
detector = BookDetector()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")


@app.get("/")
def home():
    return FileResponse(INDEX_PATH)


@app.post("/process_frame")
async def process_frame(
    file: UploadFile = File(...),
    search_text: str = Form("")
):
    """
    Receives a webcam frame and search text from frontend.
    Runs OCR using BookDetector and returns an annotated frame.
    """
    try:
        # Read the uploaded image
        contents = await file.read()
        npimg = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if frame is None:
            return JSONResponse({"error": "Invalid image data"}, status_code=400)

        # Optional resize for speed
        frame = cv2.resize(frame, (640, 480))

        # Run your OCR/Detection logic
        annotated, found_texts = detector.process_image(frame, search_text)

        # Encode image as JPEG and base64 for JSON transport
        _, encoded_img = cv2.imencode('.jpg', annotated)
        img_bytes = encoded_img.tobytes()
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')

        # Return JSON with image and any found texts
        return JSONResponse({
            'image': img_b64,
            'found_texts': found_texts
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/ping")
def ping():
    """
    Test endpoint to check backend connection.
    """
    return {"status": "ok", "message": "Backend is running fine!"}


