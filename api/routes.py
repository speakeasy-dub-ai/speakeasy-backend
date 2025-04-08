from fastapi import APIRouter, UploadFile, File
from api.endpoints import save_uploaded_audio, fetch_dubbed_audio

audio_router = APIRouter()

@audio_router.get("/")
async def root():
    return {"message": "Speakeasy Backend is running"}

@audio_router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    return await save_uploaded_audio(file)

@audio_router.get("/get-dubbed-audio")
async def get_dubbed_audio(filename: str):
    return fetch_dubbed_audio(filename)
