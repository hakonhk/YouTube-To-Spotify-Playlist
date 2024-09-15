# Spotify Playlist Tracklist Generator from YouTube DJ Sets (or just YouTube videos)

This project allows you to generate a Spotify playlist from a YouTube DJ set. It splits the audio into segments, and leverages the Shazam API to identify songs in the DJ set and the Spotify API to create a playlist with the identified tracks.
Its not flawless and often halluciantes, especially when DJs mix songs heavily or play unreleased music.

## Features

- **Download Audio**: Downloads audio from a YouTube video.
- **Analyze Audio**: Splits the audio into segments and uses Shazam to identify tracks.
- **Generate Playlist**: Creates a Spotify playlist with the identified tracks.

## Prerequisites

- Python 3.6+
- Spotify Developer Account

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/spotify-playlist-generator.git
    cd spotify-playlist-generator
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your Spotify API credentials:
    ```env
    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    ```

## Usage

1. Run the script with a YouTube URL:
    ```sh
    python main.py "https://www.youtube.com/watch?v=your_video_id"
    ```

2. The script will:
    - Download the audio from the YouTube video.
    - Segment the audio into processable sizes
    - Analyze the audio to identify tracks using Shazam.
    - Create a Spotify playlist with the identified tracks.



## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Spotipy](https://spotipy.readthedocs.io/)
- [Shazamio](https://github.com/dotX12/shazamio)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

Feel free to open an issue if you have any questions or run into any problems!
