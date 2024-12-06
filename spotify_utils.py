import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

# Spotify API kimlik bilgileri
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Spotify API bağlantısı
scope = "user-read-recently-played user-library-read user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

def get_recently_played():
    """Spotify'dan son dinlenen şarkıları alır."""
    results = sp.current_user_recently_played(limit=10)
    tracks = []
    for item in results['items']:
        track = item['track']
        tracks.append({
            'ID': track['id'],
            'Şarkı': track['name'],
            'Sanatçı': ', '.join([artist['name'] for artist in track['artists']]),
            'Albüm': track['album']['name'],
            'Kapak': track['album']['images'][0]['url'],
            'Spotify Linki': track['external_urls']['spotify']
        })
    return tracks


def add_to_favorites(track, favorites):
    """Belirtilen şarkıyı favorilere ekler."""
    if track["ID"] not in [t["ID"] for t in favorites]:
        favorites.append(track)
        return f"'{track['Şarkı']}' favorilere eklendi!"
    return None


def remove_from_favorites(track_id, favorites):
    """Favorilerden bir şarkıyı siler."""
    updated_favorites = [
        track for track in favorites if track["ID"] != track_id
    ]
    return updated_favorites, "Şarkı favorilerden kaldırıldı!"
