import asyncio
from shazamio import Shazam, exceptions
from pydub import AudioSegment
import os
import json
import time
from tqdm import tqdm

class ShazamAnalyzer:
    def __init__(self, file_path, segment_duration=60*1000, interval=30*1000, temp_dir='audio_files'):
        self.file_path = file_path
        self.segment_length = segment_duration
        self.interval = interval
        self.temp_dir = temp_dir
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    async def recognize_segment(self, segment_path):
        # Use Shazam API to recognize a song from an audio segment
        shazam = Shazam()
        try:
            out = await shazam.recognize(segment_path)
            return out
        except exceptions.NoDataApiException:
            return None
        except Exception as e:
            return str(e)

    async def run_analysis(self):
        # Analyze the entire audio stream by splitting it into segments
        # and recognizing songs in each segment
        start_time = time.time()
        dj_set = AudioSegment.from_file(self.file_path)
        total_length = len(dj_set)
        recognized_songs = []

        total_segments = (total_length - 1) // self.interval + 1
        pbar = tqdm(total=total_segments, desc="Analyzing segments")

        print(f"Total length of audio: {total_length} ms")
        print(f"Total segments to analyze: {total_segments}")

        for i in range(0, total_length, self.interval):
            segment = dj_set[i:i + self.segment_length]
            temp_file = os.path.join(self.temp_dir, f'tempsegment{i//self.interval}.mp3')
            segment.export(temp_file, format='mp3')

            print(f"Analyzing segment {i//self.interval + 1}/{total_segments}...")

            song_data = await self.recognize_segment(temp_file)
            if song_data and 'track' in song_data:
                timestamp = i // 1000
                recognized_songs.append((timestamp, song_data['track']))
                print(f"Song recognized at {timestamp}s: {song_data['track']['title']} by {song_data['track']['subtitle']}")

            os.remove(temp_file)
            pbar.update(1)

        pbar.close()
        end_time = time.time()
        print(f"Total analysis time: {end_time - start_time:.2f} seconds")
        return recognized_songs