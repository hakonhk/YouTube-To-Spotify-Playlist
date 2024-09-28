import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import aiohttp
import asyncio

load_dotenv()

class SpotifyPlaylistGenerator:
    def __init__(self, shazam_results, playlist_name):
        self.shazam_results = shazam_results
        self.playlist_name = playlist_name
        self.spotify_api = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri='http://localhost:3000',
            scope='playlist-modify-private'
        ))

    async def get_spotify_uri(self, title, artist):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.spotify.com/v1/search?q=track:{title} artist:{artist}&type=track") as response:
                if response.status == 200:
                    data = await response.json()
                    items = data['tracks']['items']
                    return items[0]['uri'] if items else None
                return None

    async def create_playlist(self):
        track_uris = await asyncio.gather(*[self.get_spotify_uri(track['title'], track['subtitle']) for track in self.shazam_results])
        track_uris = [uri for uri in track_uris if uri]

        user_id = self.spotify_api.current_user()['id']
        playlist = self.spotify_api.user_playlist_create(user_id, self.playlist_name, public=False)

        if track_uris:
            self.spotify_api.playlist_add_items(playlist['id'], track_uris)

        return playlist['external_urls']['spotify']
