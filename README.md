# Tracklist Generator: YouTube DJ-Sets to Spotify Playlists

This project automatically creates a Spotify playlist from songs identified in a YouTube video. It downloads the audio from a YouTube link, analyzes it to identify songs using Shazam, and then creates a Spotify playlist with the recognized tracks.
It is really bad and has a huge fail rate, but might improve later.

## Features

1. Download audio from YouTube videos
2. Identify songs using Shazam API
3. Create Spotify playlists with recognized songs
4. Bonus: Super inefficient processing

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- A Spotify Developer account
- Shazam API credentials (if required)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/hakonhk/Set-2-Spotify.git
   cd Set-2-Spotify
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Spotify API credentials:
   - Create a Spotify Developer account and create a new application
   - Set the redirect URI to `http://localhost:3000` in your Spotify app settings
   - Add your Spotify client ID and client secret to `main.py`

## Usage

1. Run the main script with a YouTube URL:
   ```
   python main.py "https://www.youtube.com/watch?v=your_video_id"
   ```

2. The script will download the audio, analyze it for songs, and create a Spotify playlist.

3. Follow the prompts to authorize the application with your Spotify account.

4. Once complete, the script will provide a link to your new Spotify playlist.

## Configuration

You can adjust the following parameters in `ShazamAnalyzer.py`:

- `segment_length`: Length of audio segments for analysis (in seconds)
- `overlap`: Overlap between segments (in seconds)

## Contributing

Contributions to this project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes and commit them (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature-name`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading
- [ShazamIO](https://github.com/dotX12/ShazamIO) for Shazam API integration
- [Spotipy](https://spotipy.readthedocs.io/) for Spotify API integration

## Disclaimer

This project is for educational purposes only. Ensure you comply with YouTube's and Spotify's terms of service when using this tool.
