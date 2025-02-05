from auth import authenticate_spotify
from function import *

def main():
    sp = authenticate_spotify()  

    print("Fetching Liked Songs...")
    get_liked_songs(sp)


    user_genre_playlist = input("Enter your genre to create a playlist: ")
    playlist_name = f"Liked {user_genre_playlist} Songs"

    print(f"Creating playlist: {playlist_name}...")
    playlist_id = create_playlist(sp, playlist_name)

    user_genre = input("Enter your genre to create a playlist: ").strip().lower()

    get_genre_songs(user_genre)

    

if __name__ == "__main__":
    main()
