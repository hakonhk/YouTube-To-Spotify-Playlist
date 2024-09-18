# From a Youtube video to a Spotify Playlist
## Generate Tracklists from DJ sets/mixes

This project allows you to generate a Spotify playlist from a YouTube DJ set. It splits the audio into segments, and leverages the Shazam API to identify songs in the DJ set and the Spotify API to create a playlist with the identified tracks.
Its not flawless and often halluciantes, especially when DJs mix songs heavily or play unreleased music.

## Features

- **Download Audio**: Downloads audio from a YouTube video.
- **Analyze Audio**: Splits the audio into segments and uses Shazam to identify tracks.
- **Generate Playlist**: Creates a Spotify playlist with the identified tracks.


## Limitations: These categories are often mis-recognized / creates hallucinations
- **Live Performance**
- **Heavily mixed/altered songs:** DJs often use filters, FX, Pitch Modulation, Tempo stretch, transitions, etc.
- **Quickly changing tracks:** DJs often quickly swap between different tracks (ex. on the drop)
- **Unreleased music** (random similar song will often be added)
- **Other hallucinations:** Shazam ain't perfect and it will get some songs wrong. Limitations here will be like the limitations of Shazam. *if Shazam can't find it, this can't either.*

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/hakonhk/YouTube-To-Spotify-Playlist.git
    cd YouTube-To-Spotify-Playlist
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
