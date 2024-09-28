import yt_dlp
import asyncio
from shazamio import Shazam
from pydub import AudioSegment
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioProcessor:
    def __init__(self, youtube_url):
        self.youtube_url = youtube_url
        self.buffer = BytesIO()
        self.segments = []

    async def download_audio_to_bytes(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'outtmpl': 'downloaded_audio.%(ext)s',
        }

        async def downloader():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await asyncio.to_thread(ydl.download, [self.youtube_url])

            # Write downloaded audio to buffer
            with open('downloaded_audio.mp3', 'rb') as file:
                self.buffer.write(file.read())
            self.buffer.seek(0)

        await downloader()
        return self.buffer

    def split_audio(self, segment_length_ms=60000):
        audio = AudioSegment.from_file(self.buffer, format="mp3")
        self.segments = [(i, audio[i:i + segment_length_ms]) for i in range(0, len(audio), segment_length_ms)]

    async def analyze_segment(self, segment_buffer):
        shazam = Shazam()
        try:
            # Export segment to a BytesIO buffer
            buffer = BytesIO()
            segment_buffer.export(buffer, format='mp3')
            buffer.seek(0)
            # Read bytes from the buffer
            data = buffer.read()
            result = await shazam.recognize(data=data)
            return result
        except Exception as e:
            logging.error(f"Error recognizing segment: {e}")
            return None

    async def analyze_segments(self):
        logging.info("Starting segment analysis")
        tasks = [self.analyze_segment(segment_buffer) for _, segment_buffer in self.segments]
        results = await asyncio.gather(*tasks)
        recognized_songs = [result for result in results if result]
        logging.info("Segment analysis completed")
        return recognized_songs

    async def process(self):
        await self.download_audio_to_bytes()
        self.split_audio()
        return await self.analyze_segments()
