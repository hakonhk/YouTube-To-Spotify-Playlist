import yt_dlp
import asyncio
from shazamio import Shazam
from pydub import AudioSegment
from io import BytesIO
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioProcessor:
    def __init__(self, youtube_url):
        self.youtube_url = youtube_url
        self.buffer = BytesIO()
        self.segments = []

    async def download_audio_to_bytes(self):
        class BytesIOPostProcessor(yt_dlp.postprocessor.common.PostProcessor):
            def __init__(self, buffer):
                super().__init__(None)
                self.buffer = buffer

            def run(self, information):
                file_tuple = yt_dlp.utils.sanitize_open(information['filepath'], 'rb')
                if isinstance(file_tuple, tuple):
                    f = file_tuple[0]
                else:
                    f = file_tuple
                with f:
                    self.buffer.write(f.read())
                self.buffer.seek(0)
                return [], information

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloaded_audio.%(ext)s',
        }

        async def downloader():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.add_post_processor(BytesIOPostProcessor(self.buffer), when='post_process')
                await asyncio.to_thread(ydl.download, [self.youtube_url])

        await downloader()
        return self.buffer

    def split_audio(self, segment_length_ms=60000):
        audio = AudioSegment.from_file(self.buffer, format="mp3")
        self.segments = [(i, audio[i:i + segment_length_ms]) for i in range(0, len(audio), segment_length_ms)]

    async def recognize_segment(self, segment_buffer):
        shazam = Shazam()
        try:
            result = await shazam.recognize(data=segment_buffer.getvalue())
            return result
        except Exception as e:
            logging.error(f"Error recognizing segment: {e}")
            return None

    async def analyze_segments(self):
        logging.info("Starting segment analysis")
        recognized_songs = []
        total_segments = len(self.segments)
        start_time = time.time()

        tasks = [
            self.recognize_segment(segment_buffer)
            for _, segment_buffer in self.segments
        ]

        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                recognized_songs.append(result)

        logging.info("Segment analysis completed")
        return recognized_songs

    async def run_analysis(self):
        logging.info("Starting full analysis process")
        start_time = time.time()
        self.split_audio()
        recognized_songs = await self.analyze_segments()
        end_time = time.time()
        logging.info(f"Total analysis time: {end_time - start_time:.2f} seconds")

        return recognized_songs

    async def process(self):
        await self.download_audio_to_bytes()
        return await self.run_analysis()