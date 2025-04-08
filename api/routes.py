from fastapi import APIRouter, UploadFile, File, Form
from api.endpoints import save_uploaded_audio, fetch_dubbed_audio ,save_uploaded_video ,reattach_audio_to_video

audio_router = APIRouter()

@audio_router.get("/")
async def root():
    return {"message": "Speakeasy Backend is running"}

@audio_router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    return await save_uploaded_audio(file)

@audio_router.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    """
    Endpoint to upload a video file, extract its audio, and save it.
    """
    return await save_uploaded_video(file)

@audio_router.get("/get-dubbed-audio")
async def get_dubbed_audio(filename: str):
    return fetch_dubbed_audio(filename)


@audio_router.post("/reattach-audio")
async def reattach_audio(video_filename: str = Form(...), audio_filename: str = Form(...)):
    """
    Endpoint to attach dubbed audio back to original video.
    """
    return await reattach_audio_to_video(video_filename, audio_filename)
