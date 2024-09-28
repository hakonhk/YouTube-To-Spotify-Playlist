"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import styles from '../../styles/Home.module.css';

export default function Callback() {
  const [isMounted, setIsMounted] = useState(false);
  const [status, setStatus] = useState('Waiting for Spotify callback...');
  const router = useRouter();

  useEffect(() => {
    setIsMounted(true); // Set the state to indicate that the component is mounted

    const code = new URLSearchParams(window.location.search).get('code');

    if (code) {
      setStatus('Processing Spotify authentication...');
      fetch(`http://localhost:8000/api/callback?code=${code}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error('Failed to authenticate with Spotify');
          }
          return response.json();
        })
        .then((data) => {
          if (data.message === 'Authentication successful') {
            setStatus('Authentication successful. Creating playlist...');
            return fetch('http://localhost:8000/api/create_playlist', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({ url: localStorage.getItem('youtubeLink') }),
            });
          } else {
            throw new Error('Authentication failed');
          }
        })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Failed to create playlist');
          }
          return response.json();
        })
        .then((data) => {
          if (data.playlist_url) {
            setStatus(
              `Playlist created! <a href="${data.playlist_url}" target="_blank" class="text-blue-500 underline">Open in Spotify</a>`
            );
          } else {
            setStatus('Failed to create playlist. Please try again.');
          }
        })
        .catch((error) => {
          setStatus(`An error occurred: ${error.message}. Please try again.`);
        });
    } else {
      setStatus('Invalid Spotify callback URL. Please try the authentication process again.');
    }
  }, []);

  // Only render the component after it has mounted to avoid hydration mismatch
  if (!isMounted) {
    return null;  
  }

  return (
    <div className={styles.container}>
      <h1>{status}</h1>
    </div>
  );
}