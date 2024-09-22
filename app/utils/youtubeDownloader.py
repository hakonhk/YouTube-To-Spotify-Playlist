import yt_dlp
import os
import logging

class youtubeDownloader:
    def __init__(self, download_dir='C:\\Users\\hakon\\Downloads\\New folder'):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
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
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),  # Template for output file name
            'noplaylist': True,  # Ensure only a single video is downloaded
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info and download the audio
                result = ydl.extract_info(yt_url, download=True)
                # The downloaded file might still be in a .webm container
                # The postprocessor will convert it to .mp3
                file_name = ydl.prepare_filename(result).replace('.webm', '.mp3')
                logging.info(f"Downloaded file: {file_name}")
                return file_name
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None