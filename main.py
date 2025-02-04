from auth import authenticate_spotify
from function import get_liked_songs

def main():
    sp = authenticate_spotify()  # Authenticate with Spotify
    print("Fetching Liked Songs...")

    liked_songs = get_liked_songs(sp)

    print("\nYour Liked Songs:")
    for song in liked_songs:
        print(song)

    print(f"\nTotal Liked Songs: {len(liked_songs)}")

if __name__ == "__main__":
    main()
