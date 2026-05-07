# main.py
# Modular application to easier debugging and structure
import sys
import os
import pandas as pd
from src.aiMusic import getMood, getType, suggestOne, genPlaylist
from src.fetcher import get_track_metadata
from src.userDb import save_review
from src.yt_fetcher import get_youtube_url
from src.audioAnalyzer import getBpmFromFile
from src.audioDownload import downloadAudio
from src.dataFeatures import showSorting

def main():
    """
    Start interactive menu interface for the MusicBoXD application.
    Users can add music reviews, get recommendations, create playlists, or view their review history.
    """
    print("========================================")
    print("|     🎶 Welcome to MusicBoXD 🎶       |")
    print("========================================\n")

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
                    save_review(currentTrack["name"], currentTrack["artist"], currentTrack["release_date"], vote, opinion, bpm)
                    print("success")
                case 2:
                    df = pd.read_csv('data/userOpinions.csv')
                    csvDict = df.to_dict()
                    mood = getMood()
                    gen = getType()
                    print(f"{suggestOne(csvDict, mood, gen)}\n")
                case 3:
                    df = pd.read_csv('data/userOpinions.csv')
                    csvDict = df.to_dict()
                    mood = getMood()
                    gen = getType()
                    print(f"{genPlaylist(csvDict, mood, gen)}\n")
                case 4:
                    showSorting('data/userOpinions.csv')

        except KeyboardInterrupt:
            print("\n\nShutting down MusicBoXD and cleaning data.")
            sys.exit(0)

if __name__ == "__main__":
    main()
