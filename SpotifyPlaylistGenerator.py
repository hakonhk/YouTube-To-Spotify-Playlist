import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
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

    def process_shazam_results(self, file_path):
        # Process Shazam results and get Spotify URIs for each track
        start_time = time.time()
        track_uris = []
        seen_tracks = set()
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            total_tracks = len(data)
            for idx, (timestamp, track) in enumerate(data, 1):
                title = track['title']
                artist = track['subtitle']
                track_key = f"{title}|{artist}"
                
                if track_key not in seen_tracks:
                    uri_start_time = time.time()
                    uri = self.get_spotify_uri(title, artist)
                    uri_end_time = time.time()
                    
                    if uri:
                        track_uris.append((timestamp, uri))
                        seen_tracks.add(track_key)
                        print(f"Found song {idx}/{total_tracks}: {title} by {artist} at {timestamp} seconds")
                        print(f"Time to get Spotify URI: {uri_end_time - uri_start_time:.2f} seconds")
                    else:
                        print(f"Could not find Spotify URI for: {title} by {artist}")
                else:
                    print(f"Skipping duplicate: {title} by {artist}")
        
        total_duration = time.time() - start_time
        print(f"\nTotal time to process Shazam results: {total_duration:.2f} seconds")
        print(f"Total unique songs found: {len(track_uris)}")
        
        return sorted(track_uris, key=lambda x: x[0])  # Sort by timestamp

    def create_spotify_playlist(self, track_uris, playlist_name="My Shazam Playlist"):
        # Create a new Spotify playlist and add tracks to it
        start_time = time.time()
        user_id = self.sp.me()['id']
        playlist = self.sp.user_playlist_create(user_id, playlist_name, public=False)
        uris = [uri for _, uri in track_uris]
        self.sp.playlist_add_items(playlist['id'], uris)
        total_duration = time.time() - start_time
        print(f"\nTime to create Spotify playlist: {total_duration:.2f} seconds")
        return playlist['external_urls']['spotify']



