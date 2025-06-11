from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline import process_panorama

app = FastAPI()

# Allow all origins (development only; restrict later for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/", response_class=PlainTextResponse)
async def upload(file: UploadFile = File(...)):
    filename = os.path.basename(file.filename)
    upload_path = os.path.join(UPLOAD_DIR, filename)

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Run pipeline and get the output scene name
        scene_name = process_panorama(upload_path)
        return scene_name  # frontend will use this to build the URL
    except Exception as e:
        return f"Error: {str(e)}"
