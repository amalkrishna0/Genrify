from auth import authenticate_spotify
from function import *

def main():
    sp = authenticate_spotify()  # Authenticate with Spotify
    song_id = "6EDO9iiTtwNv6waLwa1UUq"  # Replace with an actual Spotify track ID

    genres = get_song_genre(sp, song_id)
    print(f"Genres: {genres}")

if __name__ == "__main__":
    main()
