from api import get_genre_from_hf
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-private playlist-modify-public user-library-read"
    ))
    return sp


def get_liked_songs(sp):
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)  

    while results:
        for item in results["items"]:
            track = item["track"]
            liked_songs.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],  
                "id": track["id"],
                "genres": []  
            })

        results = sp.next(results) if results["next"] else None

    # Sort the songs alphabetically by album name
    liked_songs.sort(key=lambda song: song["album"].lower())  

    # Save to text file
    with open("songs.txt", "w") as file:
        for song in liked_songs:
            file.write(f"{song['name']}*{song['artist']}\n")

    return liked_songs




def get_genre_songs(user_genre):
    count = 1
    with open("songs.txt", "r") as file, open("songs_on_genre.txt", "w") as genre_file:
        for line in file:
            try:
                song_name, artist = line.strip().split("*")
            except ValueError:
                print(f"{count} Skipping invalid line: {line.strip()}")
                continue  
            
            # Use the model to predict the genre of the song
            genre_match = get_genre_from_hf(song_name, artist, user_genre)
            
            if genre_match == "YES":
                print(f"{count} - Saving {song_name} by {artist} to songs_on_genre.txt!")
                genre_file.write(f"{song_name} - {artist}\n")
            count += 1 

    


def create_playlist(sp, playlist_name):
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    return playlist["id"]


def get_track_uri(sp, song_name, artist):
    query = f"track:{song_name} artist:{artist}"
    results = sp.search(q=query, type="track", limit=1)
    
    tracks = results.get("tracks", {}).get("items", [])
    if not tracks:
        print(f"Could not find: {song_name} by {artist}")
        return None
    return tracks[0]["uri"]

import time

def add_songs_to_playlist(sp, playlist_id):
    track_uris = []

    # Read the song list from the file
    with open("songs_on_genre.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(" - ")
            if len(parts) != 2:
                print(f"Skipping invalid line: {line.strip()}")
                continue

            song_name, artist = parts
            uri = get_track_uri(sp, song_name, artist)
            if uri:
                track_uris.append(uri)

    # Batch adding songs to the playlist
    if track_uris:
        chunk_size = 100  # Spotify allows adding max 100 tracks per request
        for i in range(0, len(track_uris), chunk_size):
            batch = track_uris[i:i+chunk_size]
            try:
                sp.playlist_add_items(playlist_id, batch)
                print(f"Added {len(batch)} songs to playlist!")
                time.sleep(1)  # Avoid hitting rate limits
            except Exception as e:
                print(f"Error adding batch {i//chunk_size + 1}: {e}")
    else:
        print("No valid songs found to add!")
