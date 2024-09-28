import './globals.css';
import { ReactNode } from 'react';

export const metadata = {
  title: 'YouTube video to Spotify Playlist',
  description: 'Convert your favorite YouTube DJ sets into Spotify playlists!',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
