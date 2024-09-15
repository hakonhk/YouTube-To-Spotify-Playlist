import yt_dlp
import os
import time

class youtubeDownloader:
    def __init__(self):
        pass
    
    def download_audio(self, yt_url):
        # Configure yt-dlp options for audio download
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',  # Template for output file name
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info and download the audio
            result = ydl.extract_info(yt_url, download=True)
            file_name = ydl.prepare_filename(result)
            
            # Wait until the file is fully processed and converted to MP3
            while file_name.endswith('.webm'):
                time.sleep(1)  # Wait for 1 second before checking again
                file_name = file_name.replace('.webm', '.mp3')
            
            return file_name

# Example usage
# ytDl = youtubeDownloader()
# file_name = ytDl.download_audio("https://youtu.be/EXAMPLE")
# print(f"Downloaded file: {file_name}")