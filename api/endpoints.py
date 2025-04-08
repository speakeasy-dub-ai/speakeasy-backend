import os
import shutil
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from moviepy.editor import VideoFileClip , AudioFileClip

# Directories
UPLOAD_DIR = "uploaded_audios"
DUBBED_DIR = "dubbed_audios"
ORIGINAL_VIDEO_DIR = "original_videos"  # New folder to store original videos
DUBBED_VIDEO_DIR = "dubbed_videos"

# Create folders if they don't exist
os.makedirs(DUBBED_VIDEO_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DUBBED_DIR, exist_ok=True)
os.makedirs(ORIGINAL_VIDEO_DIR, exist_ok=True)

async def save_uploaded_audio(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "Audio uploaded successfully", "filename": file.filename}

async def save_uploaded_video(file: UploadFile):
    """
    Save the uploaded video file in 'original_videos',
    extract its audio, and save that audio in 'uploaded_audios'.
    """
    try:
        # Save original video
        video_path = os.path.join(ORIGINAL_VIDEO_DIR, file.filename)
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract audio from the video
        audio_filename = f"{os.path.splitext(file.filename)[0]}.mp3"
        audio_path = os.path.join(UPLOAD_DIR, audio_filename)
        with VideoFileClip(video_path) as video:
            video.audio.write_audiofile(audio_path)

        return {
            "message": "Video uploaded and audio extracted successfully",
            "audio_filename": audio_filename,
            "video_filename": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def fetch_dubbed_audio(filename: str):
    file_path = os.path.join(DUBBED_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav", filename=filename)
    return {"error": "Dubbed file not found"}

async def reattach_audio_to_video(video_filename: str, audio_filename: str):
    try:
        video_path = os.path.join(ORIGINAL_VIDEO_DIR, video_filename)
        audio_path = os.path.join(DUBBED_DIR, audio_filename)

        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail="Original video not found")
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Dubbed audio not found")

        # Load the video and new dubbed audio
        video = VideoFileClip(video_path)
        dubbed_audio = AudioFileClip(audio_path)

        # Set the new audio
        final_video = video.set_audio(dubbed_audio)

        # Save the final video
        output_filename = f"dubbed_{video_filename}"
        output_path = os.path.join(DUBBED_VIDEO_DIR, output_filename)
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        return FileResponse(output_path, media_type="video/mp4", filename=output_filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reattaching audio: {str(e)}")