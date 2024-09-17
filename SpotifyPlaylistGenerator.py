import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import os
from dotenv import load_dotenv
load_dotenv()
class SpotifyPlaylistGenerator:
    def __init__(self, shazam_results_file, playlistName):
        # Initialize Spotify client with OAuth authentication
        self.shazam_results_file = shazam_results_file
        self.playlistName = playlistName
        self.spotify_api = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                            redirect_uri='http://localhost:3000',
                                                            scope='playlist-modify-private'))

    def get_spotify_uri(self, title, artist):
        # Search for a track on Spotify and return its URI
        results = self.spotify_api.search(q=f"track:{title} artist:{artist}", type='track')
        print(f"Searching for: track:{title} artist:{artist}")
        items = results['tracks']['items']
        if len(items) > 0:
            return items[0]['uri']
        return None

    def process_shazam_results(self):
        # Process Shazam results and get Spotify URIs for each track
        track_uris = []
        seen_tracks = set()

        for timestamp, track in self.shazam_results_file:
            title = track['title']
            artist = track['subtitle']
            if (title, artist) not in seen_tracks:
                uri = self.get_spotify_uri(title, artist)
                if uri:
                    track_uris.append((timestamp, uri))
                    seen_tracks.add((title, artist))

        return track_uris

    def create_spotify_playlist(self, track_uris):
        # Create a new Spotify playlist and add tracks to it
        user_id = self.spotify_api.current_user()['id']
        playlist = self.spotify_api.user_playlist_create(user_id, self.playlistName, public=False)
        track_uris_only = [uri for _, uri in track_uris]
        self.spotify_api.playlist_add_items(playlist['id'], track_uris_only)
        return playlist['external_urls']['spotify']