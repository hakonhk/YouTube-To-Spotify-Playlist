import asyncio
from shazamio import Shazam, exceptions
from pydub import AudioSegment
import time
from concurrent.futures import ThreadPoolExecutor
import logging
from io import BytesIO
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShazamAnalyzer:
    def __init__(self, audio_data, progress_callback=None):
        self.audio_data = audio_data
        self.segment_length = 10 * 1000  # 10 seconds
        self.interval = 5 * 1000         # 5 seconds overlap
        self.progress_callback = progress_callback
        self.segments = []

    def segment_audio(self):
        logging.info("Starting audio segmentation")
        
        try:
            entire_track = AudioSegment.from_mp3(BytesIO(self.audio_data))
        except IOError as e:
            logging.error(f"Error reading MP3 data: {e}")
            raise ValueError("Failed to read MP3 data. The audio file may be corrupted or in an unsupported format.") from e
        except Exception as e:
            logging.error(f"Unexpected error loading audio data: {e}")
            raise ValueError(f"An unexpected error occurred while loading the audio: {str(e)}") from e
        total_length = len(entire_track)
        total_minutes = total_length // 60000
        total_seconds = (total_length % 60000) // 1000
        logging.info(f"Total length of audio: {total_minutes}m{total_seconds}s")

        def get_segment(i):
            segment = entire_track[i:i + self.segment_length]
            segment_buffer = BytesIO()
            segment.export(segment_buffer, format='mp3')
            segment_buffer.seek(0)
            return (i, segment_buffer.getvalue())

        with ThreadPoolExecutor() as executor:
            self.segments = list(executor.map(get_segment, range(0, total_length, self.interval)))

        num_segments = len(self.segments)
        logging.info(f"Total segments created: {num_segments}")
        return num_segments

    async def analyze_segment(self, index, timestamp, segment_buffer, total_segments, start_time):
        segment_start_time = time.time()
        shazam = Shazam()

        try:
            logging.info(f"Analyzing segment at timestamp {timestamp} with buffer type {type(segment_buffer)}")
            song_data = await shazam.recognize(segment_buffer)
        except Exception as e:
            if "No data" in str(e):
                song_data = None
                logging.error(f"No data found for segment at timestamp: {timestamp}")
            else:
                song_data = str(e)
                logging.error(f"Error recognizing segment at timestamp {timestamp}: {e}")
        recognized_song = None
        if song_data and 'track' in song_data:
            recognized_song = (timestamp, song_data['track'])

        # Calculate elapsed time and remaining time
        elapsed_time = time.time() - start_time
        avg_time_per_segment = elapsed_time / (index + 1)
        remaining_time = avg_time_per_segment * (total_segments - (index + 1))
        remaining_minutes, remaining_seconds = divmod(int(remaining_time), 60)
        remaining_time_str = f"{remaining_minutes}m{remaining_seconds}s"

        # Calculate segment processing time
        segment_processing_time = time.time() - segment_start_time

        # Calculate progress
        progress = (index + 1) / total_segments * 100

        # Invoke progress callback if provided
        if self.progress_callback:
            self.progress_callback(progress, remaining_time_str, segment_processing_time)
        
        # Print song and progress
        if recognized_song:
            song_title = song_data['track']['title']
            song_artist = song_data['track']['subtitle']
            timestamp_minutes = timestamp // 60000
            timestamp_seconds = (timestamp % 60000) // 1000
            
            song_title = (song_title[:10] + '...') if len(song_title) > 10 else song_title
            song_artist = (song_artist[:10] + '...') if len(song_artist) > 10 else song_artist
            logging.info(f"{progress:6.2f}%\t\"{song_title:10}\"\tby\t{song_artist:10}\tfound at\t{timestamp_minutes:02}:{timestamp_seconds:02}\tin\t{segment_processing_time:.2f}s")

    async def analyze_segments(self):
       logging.info("Starting segment analysis")
       recognized_songs = []
       total_segments = len(self.segments)
       start_time = time.time()

       tasks = [
           self.analyze_segment(index, timestamp, segment_buffer, total_segments, start_time)
           for index, (timestamp, segment_buffer) in enumerate(self.segments)
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
        self.segment_audio()
        recognized_songs = await self.analyze_segments()
        end_time = time.time()
        logging.info(f"Total analysis time: {end_time - start_time:.2f} seconds")

        return recognized_songs