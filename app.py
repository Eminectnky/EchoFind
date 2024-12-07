import streamlit as st
from spotify_utils import get_recently_played, add_to_favorites, remove_from_favorites
from gemini import gemini  

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

if "recent_tracks" not in st.session_state:
    st.session_state["recent_tracks"] = []

if "action_feedback" not in st.session_state:
    st.session_state["action_feedback"] = None

if "song_names" not in st.session_state:
    st.session_state["song_names"] = []

if "gemini_response" not in st.session_state:
    st.session_state["gemini_response"] = ""

with st.sidebar:
    st.subheader("❤️ Favoriler")
    if len(st.session_state["favorites"]) == 0:
        st.write("Henüz favorilere eklenmiş şarkı yok.")
    else:
        for track in st.session_state["favorites"]:
            st.write(f"🎵 *{track['Şarkı']}* by {track['Sanatçı']}")
            st.image(track['Kapak'], width=50)
            st.write(f"[Dinle]({track['Spotify Linki']})")
            if st.button(f"🗑️ Sil {track['Şarkı']}", key=f"remove_{track['ID']}"):
                st.session_state["favorites"], st.session_state["action_feedback"] = remove_from_favorites(
                    track["ID"], st.session_state["favorites"]
                )
                st.rerun()

    if st.button("🎶 Şarkıdan İlham Al"):
        st.session_state["gemini_response"] = gemini(st.session_state["song_names"])

    if st.session_state["gemini_response"]:
        st.write("✨ Motive Edici Notlar:")
        st.write(st.session_state["gemini_response"])

st.title("Spotify Son Dinlenen Şarkılar")
st.write("🎧 Spotify geçmişinizi yönetin, favorilerinizi ekleyin ve şarkılarınızdan ilham alın!")

if st.session_state["action_feedback"]:
    st.success(st.session_state["action_feedback"])
    st.session_state["action_feedback"] = None

if st.button("Son Dinlenen Şarkıları Göster"):
    st.session_state["recent_tracks"] = get_recently_played()
    st.session_state["song_names"] = [track['Şarkı'] for track in st.session_state["recent_tracks"]]

if st.session_state["recent_tracks"]:
    st.subheader("Son Dinlenen Şarkılar")
    for index, track in enumerate(st.session_state["recent_tracks"]):
        st.write(f"🎵 *{track['Şarkı']}* by {track['Sanatçı']}")
        st.write(f"Albüm: {track['Albüm']}")
        st.image(track['Kapak'], width=100)
        st.write(f"[Dinle]({track['Spotify Linki']})")

        if track["ID"] in [t["ID"] for t in st.session_state["favorites"]]:
            if st.button(f"🗑️ Favorilerden Sil {track['Şarkı']}", key=f"remove_{track['ID']}_{index}"):
                st.session_state["favorites"], st.session_state["action_feedback"] = remove_from_favorites(
                    track["ID"], st.session_state["favorites"]
                )
                st.rerun()
        else:
            if st.button(f"❤️ Favorilere Ekle {track['Şarkı']}", key=f"add_{track['ID']}_{index}"):
                st.session_state["action_feedback"] = add_to_favorites(
                    track, st.session_state["favorites"]
                )
                st.rerun()

        st.divider()