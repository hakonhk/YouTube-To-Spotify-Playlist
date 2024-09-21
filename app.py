from flask import Flask, request, jsonify, render_template
from SpotifyPlaylistGenerator import SpotifyPlaylistGenerator
from ShazamAnalyzer import ShazamAnalyzer
from youtubeDownloader import youtubeDownloader
import asyncio
import cProfile
import pstats
from io import StringIO
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    logging.info("Rendering index.html")
    return render_template('index.html')

@app.route('/how-it-works')
def how_it_works():
    logging.info("Rendering how-it-works.html")
    return render_template('how-it-works.html')

@app.route('/made-by')
def made_by():
    logging.info("Rendering made-by.html")
    return render_template('made-by.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    youtube_link = data['link']
    
    # Run the main function to orchestrate the entire process
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main(youtube_link))
    
    return jsonify({"message": result})

async def shazamAnalyze(file_path):
    # Analyze the audio file using Shazam
    analyzer = ShazamAnalyzer(file_path)
    results = await analyzer.run_analysis()
    return results

def playlistGen(shazam_results_file, playlistName): 
    # Generate a Spotify playlist from Shazam results
    generator = SpotifyPlaylistGenerator(shazam_results_file, playlistName)
    track_uris = generator.process_shazam_results()
    playlist_url = generator.create_spotify_playlist(track_uris)
    return f"Playlist created: {playlist_url}"

async def main(youtube_link):
    pr = cProfile.Profile()
    pr.enable()

    # Main function to orchestrate the entire process
    ytDl = youtubeDownloader()
    file_name = ytDl.download_audio(youtube_link)
    shazam_results = await shazamAnalyze(file_name)
    result = playlistGen(shazam_results, file_name.replace('.mp3', ''))

    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    return result

if __name__ == '__main__':
    print("Starting the Flask app with Flask's built-in server...")
    logging.info("Starting the Flask app with Flask's built-in server...")
    app.run(host='127.0.0.1', port=5000, debug=True)
    logging.info("Flask app is running.")
    print("Flask app is running.")