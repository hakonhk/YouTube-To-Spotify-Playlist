"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import styles from '../styles/Home.module.css';

export default function Home() {
  const [redirecting, setRedirecting] = useState(false);

  const handleAuth = async () => {
    setRedirecting(true);
    const response = await fetch('http://localhost:8000/api/get_spotify_auth_url');
    const data = await response.json();
    window.location.href = data.auth_url;
  };

  return (
    <div className={`${styles.container} min-h-screen flex flex-col items-center justify-center`}>
      <main className={`${styles.main} flex flex-col items-center justify-center w-full px-20 text-center`}>
        <h1 className={styles.title}>YouTube to Spotify Playlist</h1>
        <p className={styles.description}>Convert your favorite YouTube DJ sets into Spotify playlists!</p>

        <button
          onClick={handleAuth}
          className={styles.button}
          disabled={redirecting}
        >
          {redirecting ? 'Redirecting to Spotify...' : 'Authenticate with Spotify'}
        </button>
      </main>
    </div>
  );
}
