from SpotifyPlaylistGenerator import SpotifyPlaylistGenerator
from ShazamAnalyzer import ShazamAnalyzer
from youtubeDownloader import youtubeDownloader
import asyncio
import sys

async def shazamAnalyze(file_path):
    # Analyze the audio file using Shazam
    analyzer = ShazamAnalyzer(file_path)
    results = await analyzer.run_analysis()
    return results

def playlistGen(shazam_results_file, playlistName): 
    # Generate a Spotify playlist from Shazam results
    generator = SpotifyPlaylistGenerator(shazam_results_file, playlistName) #TODO: Further encapsulation?
    track_uris = generator.process_shazam_results()
    playlist_url = generator.create_spotify_playlist(track_uris)
    print(f"Playlist created: {playlist_url}")
    
    print("\nPlaylist order:")
    for timestamp, uri in track_uris:
        track_info = generator.spotify_api.track(uri)
        print(f"{timestamp} seconds: {track_info['name']} by {track_info['artists'][0]['name']}")

async def main(youtube_link):
    # Main function to orchestrate the entire process
    ytDl = youtubeDownloader()
    file_name = ytDl.download_audio(youtube_link)
    shazam_results = await shazamAnalyze(file_name)
    playlistGen(shazam_results, file_name.replace('.mp3', ''))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_link = sys.argv[1]
        asyncio.run(main(youtube_link))
    else:
        print("Please provide a YouTube URL as a command-line argument.")
        print("Usage: python main.py \"https://www.youtube.com/watch?v=your_video_id\"")