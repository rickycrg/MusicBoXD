import csv
import os

db_file = "data/userOpinions.csv"

def save_review(song_name, artist, vote, opinion, bpm):
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(db_file)   

    with open(db_file, mode='a', newline='', encoding='utf8') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["song name", "artist", "bpm", "vote", "opinion"])

        writer.writerow([song_name, artist, bpm, vote, opinion])

    print(f"opinion to {song_name} submitted!")

