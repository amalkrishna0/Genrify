from auth import authenticate_spotify
from function import get_liked_songs

def main():
    sp = authenticate_spotify()  
    print("Fetching Liked Songs...")

    get_liked_songs(sp)



if __name__ == "__main__":
    main()
