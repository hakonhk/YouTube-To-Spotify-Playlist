import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

class SpotifyPlaylistGenerator:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        # Initialize Spotify client with OAuth authentication
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope=scope))

    def get_spotify_uri(self, title, artist):
        # Search for a track on Spotify and return its URI
        results = self.sp.search(q=f"track:{title} artist:{artist}", type='track')
        print(f"Searching for: track:{title} artist:{artist}")
        items = results['tracks']['items']
        if len(items) > 0:
            return items[0]['uri']
        return None

    def process_shazam_results(self, shazam_results):
        # Process Shazam results and get Spotify URIs for each track
        track_uris = []
        seen_tracks = set()

        for timestamp, track in shazam_results:
            title = track['title']
            artist = track['subtitle']
            if (title, artist) not in seen_tracks:
                uri = self.get_spotify_uri(title, artist)
                if uri:
                    track_uris.append((timestamp, uri))
                    seen_tracks.add((title, artist))

        return track_uris

    def create_spotify_playlist(self, track_uris, playlist_name="My Shazam Playlist"):
        # Create a new Spotify playlist and add tracks to it
        user_id = self.sp.current_user()['id']
        playlist = self.sp.user_playlist_create(user_id, playlist_name, public=False)
        track_uris_only = [uri for _, uri in track_uris]
        self.sp.playlist_add_items(playlist['id'], track_uris_only)
        return playlist['external_urls']['spotify']



