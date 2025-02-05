def get_liked_songs(sp):
    liked_songs = []
    results = sp.current_user_saved_tracks(limit=50)  # First batch

    while results:
        for item in results["items"]:
            track = item["track"]
            liked_songs.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],  # Fetch album name
                "id": track["id"],
                "genres": []  # Placeholder for genres
            })

        results = sp.next(results) if results["next"] else None

    # Sort the songs alphabetically by album name
    liked_songs.sort(key=lambda song: song["album"].lower())  # Case-insensitive sorting

    # Save to text file
    with open("songs.txt", "w", encoding="utf-8") as file:
        for song in liked_songs:
            file.write(f"{song['album']} - {song['name']} - {song['artist']} (ID: {song['id']})\n")

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
