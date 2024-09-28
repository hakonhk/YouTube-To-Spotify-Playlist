# spotify_auth.py
import os
from dotenv import load_dotenv
import aiohttp
from urllib.parse import urlencode

load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:3000/callback"  # match exactly what is in Spotify Developer Dashboard

def get_spotify_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "playlist-modify-private",
    }
    return f"https://accounts.spotify.com/authorize?{urlencode(params)}"

async def get_spotify_token(code):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data["access_token"]
    return None

async def refresh_token(refresh_token):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("access_token")
    return None
