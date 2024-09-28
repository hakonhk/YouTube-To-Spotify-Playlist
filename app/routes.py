from flask import Blueprint, render_template, request, jsonify
from flask_socketio import emit
from .utils.SpotifyPlaylistGenerator import SpotifyPlaylistGenerator
from .utils.AudioProcessor import AudioProcessor
import asyncio
from tqdm import tqdm
from app import socketio  # Import socketio from app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    youtube_link = data['link']
    
    # Run the main function to orchestrate the entire process
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result, estimated_time = loop.run_until_complete(main_analysis(youtube_link))
    
    return jsonify({"message": result, "estimated_time": estimated_time})

async def shazam_analyze(audio_processor):
    def progress_callback(progress, estimated_time, segment_processing_time):
        socketio.emit('progress_update', {'progress': progress, 'estimated_time': estimated_time, 'segment_processing_time': segment_processing_time})

    results = await audio_processor.run_analysis()
    return results

def playlist_gen(shazam_results, playlist_name):
    generator = SpotifyPlaylistGenerator(shazam_results, playlist_name)
    track_uris = generator.process_shazam_results()
    playlist_url = generator.create_spotify_playlist(track_uris)
    return f"Playlist created: {playlist_url}"

async def main_analysis(youtube_link):
    audio_processor = AudioProcessor(youtube_link)
    await audio_processor.download_audio_to_bytes()
    
    # Initialize progress bar
    with tqdm(total=100, desc="Overall Progress") as pbar:
        # Downloading audio
        pbar.update(10)
        
        # Shazam analysis
        shazam_results = await shazam_analyze(audio_processor)
        pbar.update(70)
        
        # Playlist generation
        result = playlist_gen(shazam_results, audio_processor.youtube_url)
        pbar.update(20)
    
    return result, "Estimated time not available"

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")