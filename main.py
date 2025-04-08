from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import audio_router


app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your API routes
app.include_router(audio_router)
