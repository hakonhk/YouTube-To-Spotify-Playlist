import asyncio
from shazamio import Shazam, exceptions
from pydub import AudioSegment
import os
import json
import time
from tqdm import tqdm

class ShazamAnalyzer:
    def __init__(self, file_path, segment_length=15*60*1000, interval=60*1000):
        # Initialize with file path and analysis parameters
        # segment_length: length of audio segment to analyze (default: 15 minutes)
        # interval: time between start of each segment (default: 1 minute)
        self.file_path = file_path
        self.segment_length = segment_length
        self.interval = interval

    async def recognize_song(self, segment_path):
        # Use Shazam API to recognize a song from an audio segment
        shazam = Shazam()
        try:
            out = await shazam.recognize(segment_path)
            return out
        except exceptions.NoDataApiException:
            return "Ingen data funnet"
        except Exception as e:
            return str(e)

    async def analyze_stream(self):
        # Analyze the entire audio stream by splitting it into segments
        # and recognizing songs in each segment
        start_time = time.time()
        dj_set = AudioSegment.from_file(self.file_path)
        total_length = len(dj_set)
        recognized_songs = []

        total_segments = (total_length - 1) // self.interval + 1
        pbar = tqdm(total=total_segments, desc="Analyzing segments")

        for i in range(0, total_length, self.interval):
            segment_start_time = time.time()
            segment = dj_set[i:i + self.segment_length]
            temp_file = f'temp_segment_{i//self.interval}.mp3'
            segment.export(temp_file, format='mp3')

            song_data = await self.recognize_song(temp_file)
            if 'track' in song_data:
                timestamp = i // 1000  # Konverter til sekunder
                recognized_songs.append((timestamp, song_data['track']))
                print(f"Song recognized at {timestamp}s: {song_data['track']['title']} by {song_data['track']['subtitle']}")

            os.remove(temp_file)
            
            segment_end_time = time.time()
            segment_duration = segment_end_time - segment_start_time
            print(f"Segment {i//self.interval + 1}/{total_segments} processed in {segment_duration:.2f} seconds")
            
            pbar.update(1)

        pbar.close()
        total_duration = time.time() - start_time
        print(f"\nTotal Shazam analysis time: {total_duration:.2f} seconds")
        print(f"Total songs recognized: {len(recognized_songs)}")

        return recognized_songs
    async def run_analysis(self):
        # Run the complete Shazam analysis and save results to a JSON file
        print("Starting Shazam analysis...")
        recognized_songs = await self.analyze_stream()
        
        with open(f'{self.file_path}_shazam_results.json', 'w') as f:
            json.dump(recognized_songs, f)

        print(f"Shazam analysis completed. Results saved in '{self.file_path}_shazam_results.json'")