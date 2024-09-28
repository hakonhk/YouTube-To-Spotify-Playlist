import yt_dlp
import asyncio
from shazamio import Shazam
from pydub import AudioSegment
from io import BytesIO

async def download_audio_to_bytes(youtube_url):
    buffer = BytesIO()
    
    # Define custom postprocessor to catch data being written out
    class BytesIOPostProcessor(yt_dlp.postprocessor.common.PostProcessor):
        def run(self, information):
            # Use sanitize_open and handle the tuple correctly
            file_tuple = yt_dlp.utils.sanitize_open(information['filepath'], 'rb')
            if isinstance(file_tuple, tuple):
                f = file_tuple[0]
            else:
                f = file_tuple
            with f:
                buffer.write(f.read())
            buffer.seek(0)
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
            ydl.add_post_processor(BytesIOPostProcessor(), when='post_process')
            await asyncio.to_thread(ydl.download, [youtube_url])

    await downloader()

    return buffer

def split_audio(audio_bytes_io, segment_length_ms=60000):
    audio = AudioSegment.from_file(audio_bytes_io, format="mp3")
    num_segments = len(audio) // segment_length_ms
    
    for i in range(num_segments):
        start_time = i * segment_length_ms
        end_time = start_time + segment_length_ms
        segment = audio[start_time:end_time]
        segment_buffer = BytesIO()
        segment.export(segment_buffer, format="mp3")
        segment_buffer.seek(0)
        yield segment_buffer

async def recognize_segment(segment_bytes_io):
    shazam = Shazam()
    try:
        recognition = await shazam.recognize(data=segment_bytes_io.getvalue())
    except Exception as e:
        print(f"Error recognizing song: {e}")
        return {}

    return recognition

async def main():
    youtube_url = 'https://youtu.be/hb0XLX0b4Y4?si=rzZJSFuhcEUeuqgo'  # Replace with your video's URL
    audio_buffer = await download_audio_to_bytes(youtube_url)
    
    # Split the audio buffer into segments and recognize songs in each segment
    for segment_buffer in split_audio(audio_buffer):
        result = await recognize_segment(segment_buffer)
        if 'track' in result:
            track_info = result['track']
            print(f"Title: {track_info['title']}, Artist: {track_info['subtitle']}")
        else:
            print("Song in this segment could not be recognized.")

if __name__ == "__main__":
    asyncio.run(main())


