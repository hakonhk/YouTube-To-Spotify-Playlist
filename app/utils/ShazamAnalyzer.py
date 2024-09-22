import asyncio
from shazamio import Shazam, exceptions
from pydub import AudioSegment
import os
import time
from concurrent.futures import ThreadPoolExecutor
import logging
import psutil
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ShazamAnalyzer:
    def __init__(self, file_path, segment_length=60*1000, interval=60*1000, temp_dir='C:\\Users\\hakon\\Downloads\\New folder', progress_callback=None):
        self.file_path = file_path
        self.segment_length = segment_length
        self.interval = interval
        self.temp_dir = temp_dir
        self.progress_callback = progress_callback
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        self.segments = []

    def segment_audio(self):
        logging.info("Starting audio segmentation")
        
        if not self.file_path or not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Audio file not found: {self.file_path}")
        
        entireTrack = AudioSegment.from_file(self.file_path)
        total_length = len(entireTrack)
        total_minutes = total_length // 60000
        total_seconds = (total_length % 60000) // 1000
        logging.info(f"Total length of audio: {total_minutes}m{total_seconds}s")

        def export_segment(i):
            segment = entireTrack[i:i + self.segment_length]
            temp_file = os.path.join(self.temp_dir, f'tempsegment{i//self.interval}.mp3')
            segment.export(temp_file, format='mp3')
            return (i, temp_file)

        with ThreadPoolExecutor() as executor:
            self.segments = list(executor.map(export_segment, range(0, total_length, self.interval)))

        num_segments = len(self.segments)
        logging.info(f"Total segments created: {num_segments}")

        # Estimate the time based on average processing time per segment
        average_processing_time_per_segment = 15  # Assuming each segment takes ~15 seconds to process
        estimated_time_seconds = num_segments * average_processing_time_per_segment
        estimated_time_minutes, estimated_time_seconds = divmod(estimated_time_seconds, 60)
        estimated_time_str = f"~{estimated_time_minutes}m{estimated_time_seconds}s"
        logging.info(f"Estimated analysis time: {estimated_time_str}")

        return estimated_time_str

    """ async def recognize_segment(self, segment_path):
        shazam = Shazam()
        try:
            out = await shazam.recognize(segment_path)
            return out
        except exceptions.NoDataApiException:
            logging.error(f"No data found for segment: {segment_path}")
            return None
        except Exception as e:
            logging.error(f"Error recognizing segment {segment_path}: {e}")
            return str(e) """

    async def analyze_segment(self, index, timestamp, segment_path, total_segments, start_time):
        segment_start_time = time.time()

        shazam = Shazam()
        try:
            song_data = await shazam.recognize(segment_path)
        except exceptions.NoDataApiException:
            song_data = None
            logging.error(f"No data found for segment: {segment_path}")
        except Exception as e:
            song_data = str(e)
            logging.error(f"Error recognizing segment {segment_path}: {e}")

        recognized_song = None
        if song_data and 'track' in song_data:
            recognized_song = (timestamp, song_data['track'])

        os.remove(segment_path)

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

        return recognized_song

    async def analyze_segments(self):
        logging.info("Starting segment analysis")
        recognized_songs = []
        total_segments = len(self.segments)
        start_time = time.time()

        concurrency_level = 10  # Initial concurrency level
        semaphore = asyncio.Semaphore(concurrency_level)
        max_concurrency = 30  # Set a maximum concurrency level
        stabilization_interval = 5  # Time interval in seconds to stabilize concurrency adjustments
        last_adjustment_time = time.time()

        async def analyze_with_semaphore(index, timestamp, segment_path):
            async with semaphore:
                return await self.analyze_segment(index, timestamp, segment_path, total_segments, start_time)

        tasks = [analyze_with_semaphore(index, timestamp, segment_path) for index, (timestamp, segment_path) in enumerate(self.segments)]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                recognized_songs.append(result)

                # Monitor system resources and adjust concurrency level periodically
                current_time = time.time()
                if current_time - last_adjustment_time >= stabilization_interval:
                    cpu_usage = psutil.cpu_percent()
                    memory_usage = psutil.virtual_memory().percent

                    adjustment_info = ""
                    if cpu_usage > 80 or memory_usage > 80:
                        concurrency_level = max(1, concurrency_level - 1)
                        semaphore = asyncio.Semaphore(concurrency_level)
                        adjustment_info = f"Reducing concurrency level to {concurrency_level}"
                    elif cpu_usage < 50 and memory_usage < 50 and concurrency_level < max_concurrency:
                        concurrency_level += 1
                        semaphore = asyncio.Semaphore(concurrency_level)
                        adjustment_info = f"Increasing concurrency level to {concurrency_level}"

                    logging.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%. {adjustment_info}")

                    last_adjustment_time = current_time

        logging.info("Segment analysis completed")
        return recognized_songs

    async def run_analysis(self):
        logging.info("Starting full analysis process")
        start_time = time.time()
        estimated_time = self.segment_audio()
        recognized_songs = await self.analyze_segments()
        end_time = time.time()
        logging.info(f"Total analysis time: {end_time - start_time:.2f} seconds")

        assert os.path.exists(self.file_path)
        os.remove(self.file_path)
        logging.info(f"Deleted original audio file: {self.file_path}")

        # Delete __pycache__ directories
        """ self.delete_pycache(os.path.join(os.getcwd(), 'app'))
        self.delete_pycache(os.path.join(os.getcwd(), 'utils')) """

        return recognized_songs, estimated_time
    
"""     def delete_pycache(directory):
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    shutil.rmtree(os.path.join(root, dir_name)) """