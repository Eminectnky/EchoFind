import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

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


st.title("Spotify Son Dinlenen Şarkılar")
st.write("Spotify API ile son dinlediğiniz şarkıları listeleyen bir uygulama.")


def get_recently_played():
    results = sp.current_user_recently_played(limit=10)
    tracks = []
    for item in results['items']:
        track = item['track']
        tracks.append({
            'Şarkı': track['name'],
            'Sanatçı': ', '.join([artist['name'] for artist in track['artists']]),
            'Albüm': track['album']['name'],
            'Kapak': track['album']['images'][0]['url'],
            'Spotify Linki': track['external_urls']['spotify']
        })
    return tracks

if st.button("Son Dinlenen Şarkıları Göster"):
    tracks = get_recently_played()
    for track in tracks:
        st.write(f"🎵 {track['Şarkı']} by {track['Sanatçı']}")
        st.write(f"Albüm: {track['Albüm']}")
        st.image(track['Kapak'], width=100)
        st.write(f"[Dinle]({track['Spotify Linki']})")
