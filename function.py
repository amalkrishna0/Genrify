from api import get_genre_from_hf
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
    with open("songs.txt", "r") as file, open("songs_on_genre.txt", "w") as genre_file:
        for line in file:
            song_name, artist = line.strip().split("*")
            
            # Use the model to predict the genre of the song
            genre_match = get_genre_from_hf(song_name, artist, user_genre)
            
            if genre_match == "YES":
                print(f"Saving {song_name} by {artist} to songs_on_genre.txt!")
                genre_file.write(f"{song_name} - {artist}\n")