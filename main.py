from SpotifyPlaylistGenerator import SpotifyPlaylistGenerator
from ShazamAnalyzer import ShazamAnalyzer
from youtubeDownloader import youtubeDownloader
import asyncio
import time

async def shazamAnalyze(file_path):
    # Analyze the audio file using Shazam
    analyzer = ShazamAnalyzer(file_path)
    await analyzer.run_analysis()

def playlistGen(shazam_results_file, playlistName):
    # Generate a Spotify playlist from Shazam results
    SPOTIPY_CLIENT_ID = 'X' # TODO: Add your Spotify client ID
    SPOTIPY_CLIENT_SECRET = 'X' # TODO: Add your Spotify client secret
    SPOTIPY_REDIRECT_URI = 'http://localhost:3000'
    SCOPE = 'playlist-modify-private'

    generator = SpotifyPlaylistGenerator(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPE)
    track_uris = generator.process_shazam_results(shazam_results_file)
    playlist_url = generator.create_spotify_playlist(track_uris, playlistName)
    print(f"Playlist created: {playlist_url}")
    
    print("\nPlaylist order:")
    for timestamp, uri in track_uris:
        track_info = generator.sp.track(uri)
        print(f"{timestamp} seconds: {track_info['name']} by {track_info['artists'][0]['name']}")

def main(youtube_link):  
    # Main function to orchestrate the entire process
    ytDl = youtubeDownloader()
    file_path = ytDl.download_audio(youtube_link)
    print(f"Downloaded file: {file_path}")

    shazam_start_time = time.time()
    asyncio.run(shazamAnalyze(file_path))
    shazam_end_time = time.time()
    print(f"Total Shazam analysis time: {shazam_end_time - shazam_start_time:.2f} seconds")

    shazam_results_file = f'{file_path}_shazam_results.json'
    
    spotify_start_time = time.time()
    playlistGen(shazam_results_file, file_path.replace('.mp3', ''))
    
    spotify_end_time = time.time()
    print(f"Total Spotify playlist generation time: {spotify_end_time - spotify_start_time:.2f} seconds")

    print(f"\nTotal execution time: {spotify_end_time - shazam_start_time:.2f} seconds")

if __name__ == "__main__":
    main("https://youtu.be/hb0XLX0b4Y4?si=adYYBjM6oVnbTWJ4") # TODO: Add your YouTube link here
