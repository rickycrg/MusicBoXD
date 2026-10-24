# main.py
# Modular application to easier debugging and structure
import sys
import os
from getpass import getpass
import requests
from src.d1 import D1Error
from src.aiMusic import getMood, getType, suggestOne, genPlaylist
from src.fetcher import get_track_metadata
from src.userDb import save_review, get_reviews, login_user, register_user
from src.yt_fetcher import get_youtube_url
from src.audioAnalyzer import getBpmFromFile
from src.audioDownload import downloadAudio
from src.dataFeatures import showSorting

def authenticate():
    """
    Ask the user to log in or create an account, return the user_id.
    """
    while True:
        print("[1] - Login")
        print("[2] - Register")
        print("[0] - EXIT\n")
        choice = input("insert menu voice: ")
        match(choice):
            case "0":
                print("shutting down MusicBoXD.")
                sys.exit(0)
            case "1":
                username = input("username: ")
                user_id = login_user(username, getpass("password: "))
                if user_id:
                    print(f"welcome back {username}!\n")
                    return user_id
                print("wrong username or password.\n")
            case "2":
                username = input("username: ")
                email = input("email: ")
                password = getpass("password: ")
                if not username or not email or not password:
                    print("username, email and password are required.\n")
                    continue
                name = input("name (optional): ") or None
                surname = input("surname (optional): ") or None
                phone = input("phone number (optional): ") or None
                user_id = register_user(username, email, password, name, surname, phone)
                if user_id:
                    print(f"account created, welcome {username}!\n")
                    return user_id
                print("username or email already in use.\n")
            case _:
                print("invalid menu voice, choose between 0 and 2.\n")

def main():
    """
    Start interactive menu interface for the MusicBoXD application.
    Users can add music reviews, get recommendations, create playlists, or view their review history.
    """
    print("========================================")
    print("|     🎶 Welcome to MusicBoXD 🎶       |")
    print("========================================\n")

    try:
        user_id = authenticate()
    except KeyboardInterrupt:
        print("\n\nShutting down MusicBoXD.")
        sys.exit(0)

    while True:
        print("============ MENU ============\n")
        print("[1] - New Opinion")
        print("[2] - Suggest a Music")
        print("[3] - Make a Playlist")
        print("[4] - Show List of Reviews")
        print("[0] - EXIT\n")
        try: 
            menuW = input("insert menu voice: ")
            menu = int(menuW)
            match(menu):
                case 0:
                    print("shutting down MusicBoXD and cleaning data.")
                    sys.exit(0)
                case 1:
                    search = input("insert the new music name: ")
                    currentTrack = get_track_metadata(search)
                    if not currentTrack:
                        print("music does not exists")
                        continue
                    url = get_youtube_url(currentTrack["name"], currentTrack["artist"])
                    if not url:
                        print("url not found")
                        continue
                    file = downloadAudio(url)
                    if file:
                        bpm = getBpmFromFile(file)
                        os.remove(file)
                    else:
                        print("Download failed, skipping bpm calculation.")
                        bpm = -1.0

                    vote = -1
                    while vote < 1 or vote > 5:
                        try:
                            vote = int(input("insert vote (1 to 5): "))
                        except ValueError:
                            print("invalid input, enter a number: ")

                    opinion = input("insert opinion about the music: ")
                    save_review(user_id, currentTrack, vote, opinion, bpm)
                    print("success")
                case 2:
                    taste = get_reviews(user_id).to_dict()
                    mood = getMood()
                    gen = getType()
                    print(f"{suggestOne(taste, mood, gen)}\n")
                case 3:
                    taste = get_reviews(user_id).to_dict()
                    mood = getMood()
                    gen = getType()
                    print(f"{genPlaylist(taste, mood, gen)}\n")
                case 4:
                    showSorting(get_reviews(user_id))
                case _:
                    print("invalid menu voice, choose between 0 and 4.\n")

        except ValueError:
            print("invalid input, enter a number.\n")
        except (D1Error, requests.RequestException) as e:
            print(f"database error: {e}\n")
        except KeyboardInterrupt:
            print("\n\nShutting down MusicBoXD and cleaning data.")
            sys.exit(0)

if __name__ == "__main__":
    main()
