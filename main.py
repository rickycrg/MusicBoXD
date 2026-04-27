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

def main():
    """
    Start interface of the application
    """
    print("========================================")
    print("      🎶 Welcome to MusicBoXD 🎶        ")
    print("========================================\n")
    

    while True:
        """
        Interactive basic menu to let the user decide what does he want to do
        """
        print("============ MENU ============\n")    
        print("[1] - New Opinion")
        print("[2] - Suggest a Music")
        print("[3] - Make a Playlist")
        print("[0] - EXIT\n")
        try: 
            menuW = input("insert menu voice: ")
            menu = int(menuW)
            if 0 <= menu <= 3:
                #shutdown
                if menu == 0:
                    print("shutting down MusicBoXD")
                    sys.exit(0)
                elif menu == 1:
                    search = input("insert the new music name: ")
                    currentTrack = get_track_metadata(search)
                    #edgecases to debug if the function dont works
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
                    try: 

                        vote = -1
                        #Getting user's opinion
                        while vote < 1 or vote > 5:
                            try:
                                vote = int(input("insert vote (1 to 5): "))
                            except ValueError:
                                print("invalid input, enter a number: ")

                        opinion = input("insert opinion about the music: ")
                        save_review(currentTrack["name"], currentTrack["artist"], vote, opinion, bpm)
                    finally:
                        if file and os.path.exists(file):
                            os.remove(file)
                            print("success")
                elif menu == 2:
                    # Using pandas to convert the csv file to a Dict, to make the AI interpretate the data
                    df = pd.read_csv('data/userOpinions.csv')
                    csvDict = df.to_dict
                    mood = getMood()
                    gen = getType()
                    print(f"{suggestOne(csvDict, mood, gen)}\n")
                elif menu == 3:
                    df = pd.read_csv('data/userOpinions.csv')
                    csvDict = df.to_dict
                    mood = getMood()
                    gen = getType()
                    print(f"{genPlaylist(csvDict, mood, gen)}\n")
                    

        # Consent the cntrl+v without bugging
        except KeyboardInterrupt:
            print("\n\nShutting down MusicBoXD. See you next time!")
            sys.exit(0)

if __name__ == "__main__":
    main()