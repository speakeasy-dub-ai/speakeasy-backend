import os
import shutil
from fastapi import UploadFile
from fastapi.responses import FileResponse

UPLOAD_DIR = "uploaded_audios"
DUBBED_DIR = "dubbed_audios"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DUBBED_DIR, exist_ok=True)

async def save_uploaded_audio(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Audio uploaded successfully", "filename": file.filename}

def fetch_dubbed_audio(filename: str):
    file_path = os.path.join(DUBBED_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav", filename=filename)
    return {"error": "Dubbed file not found"}
