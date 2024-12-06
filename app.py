import streamlit as st
from spotify_utils import get_recently_played, add_to_favorites, remove_from_favorites

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

if "recent_tracks" not in st.session_state:
    st.session_state["recent_tracks"] = []

if "action_feedback" not in st.session_state:
    st.session_state["action_feedback"] = None  


with st.sidebar:
    st.subheader("❤️ Favoriler")
    if len(st.session_state["favorites"]) == 0:
        st.write("Henüz favorilere eklenmiş şarkı yok.")
    else:
        for track in st.session_state["favorites"]:
            st.write(f"🎵 **{track['Şarkı']}** by {track['Sanatçı']}")
            st.image(track['Kapak'], width=50)
            st.write(f"[Dinle]({track['Spotify Linki']})")
            if st.button(f"🗑️ Sil {track['Şarkı']}", key=f"remove_{track['ID']}"):
                st.session_state["favorites"], st.session_state["action_feedback"] = remove_from_favorites(
                    track["ID"], st.session_state["favorites"]
                )


st.title("Spotify Son Dinlenen Şarkılar")
st.write("Spotify API ile son dinlediğiniz şarkıları listeleyin ve favorilere ekleyin.")

if st.session_state["action_feedback"]:
    st.success(st.session_state["action_feedback"])
    st.session_state["action_feedback"] = None  

if st.button("Son Dinlenen Şarkıları Göster"):
    st.session_state["recent_tracks"] = get_recently_played()

if st.session_state["recent_tracks"]:
    st.subheader("Son Dinlenen Şarkılar")
    for index, track in enumerate(st.session_state["recent_tracks"]):
        st.write(f"🎵 **{track['Şarkı']}** by {track['Sanatçı']}")
        st.write(f"Albüm: *{track['Albüm']}*")
        st.image(track['Kapak'], width=100)
        st.write(f"[Dinle]({track['Spotify Linki']})")

        # Favorilere Ekleme veya Silme
        if track["ID"] in [t["ID"] for t in st.session_state["favorites"]]:
            # Eğer favorilerdeyse "Sil" butonu
            if st.button(f"🗑️ Favorilerden Sil {track['Şarkı']}", key=f"remove_{track['ID']}_{index}"):
                st.session_state["favorites"], st.session_state["action_feedback"] = remove_from_favorites(
                    track["ID"], st.session_state["favorites"]
                )
        else:
            # Eğer favorilerde değilse "Ekle" butonu
            if st.button(f"❤️ Favorilere Ekle {track['Şarkı']}", key=f"add_{track['ID']}_{index}"):
                st.session_state["action_feedback"] = add_to_favorites(
                    track, st.session_state["favorites"]
                )

        st.divider()
