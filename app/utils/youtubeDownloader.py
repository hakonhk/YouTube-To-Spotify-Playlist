import yt_dlp
import logging
from io import BytesIO
import os

class youtubeDownloader:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
    
    def download_audio(self, yt_url):
        # Configure yt-dlp options for direct audio download
        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best available audio format
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Convert the audio to mp3 format
                'preferredquality': '192',  # Set the quality of the mp3 file
            }],
            'outtmpl': '%(title)s.%(ext)s',  # Template for output file name
            'noplaylist': True,  # Ensure only a single video is downloaded
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info and download the audio
                result = ydl.extract_info(yt_url, download=True)
                file_path = ydl.prepare_filename(result).replace('.webm', '.mp3')
                logging.info(f"Downloaded file path: {file_path}")
                
                # Read the downloaded file into memory
                with open(file_path, 'rb') as f:
                    audio_data = f.read()
                
                logging.info("Downloaded audio data in memory")
                
                # Clean up the downloaded file
                os.remove(file_path)
                
                return audio_data, result['title']
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None, None