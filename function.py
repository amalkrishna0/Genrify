def get_liked_songs(sp):
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)  # First batch

    while results:
        for item in results["items"]:
            track = item["track"]
            liked_songs.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "id": track["id"],
                "genres": []  # Placeholder, as Spotify API doesn't provide genres for individual tracks
            })

        results = sp.next(results) if results["next"] else None

    return liked_songs


def get_song_genre(sp, song_id):
    # Fetch track details
    track_info = sp.track(song_id)
    
    # Get the first artist's ID
    artist_id = track_info["artists"][0]["id"]
    
    # Fetch artist details
    artist_info = sp.artist(artist_id)
    
    # Extract genres
    genres = artist_info.get("genres", [])

    return genres
