import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from spotify_auth import get_spotify_auth_url, get_spotify_token
from app.utils.AudioProcessor import AudioProcessor
from app.utils.SpotifyPlaylistGenerator import SpotifyPlaylistGenerator
import asyncio

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class YouTubeLink(BaseModel):
    url: str

@app.get("/api/get_spotify_auth_url")
async def get_auth_url():
    auth_url = get_spotify_auth_url()
    return {"auth_url": auth_url}

@app.post("/api/process")
async def process_link(youtube_link: YouTubeLink):
    logging.info(f"Processing link: {youtube_link.url}")
    auth_url = get_spotify_auth_url()
    return {"auth_url": auth_url}

@app.get("/api/callback")
async def spotify_callback(code: str):
    logging.info(f"Received callback with code: {code}")
    token = await get_spotify_token(code)
    if not token:
        logging.error("Authentication failed")
        raise HTTPException(status_code=400, detail="Authentication failed")
    logging.info("Authentication successful")
    return {"message": "Authentication successful"}

@app.post("/api/create_playlist")
async def create_playlist(youtube_link: YouTubeLink):
    logging.info(f"Creating playlist from link: {youtube_link.url}")
    try:
        processor = AudioProcessor(youtube_link.url)
        recognized_songs = await processor.process()
        playlist_generator = SpotifyPlaylistGenerator(recognized_songs, "Generated Playlist")
        playlist_url = await playlist_generator.create_playlist()
        logging.info(f"Playlist created: {playlist_url}")
        return {"playlist_url": playlist_url}
    except Exception as e:
        logging.error(f"Error creating playlist: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the playlist.")
