import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv

load_dotenv()

def get_track_metadata(search_query):

    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id or not secret:
        raise ValueError("Missing Spotify credentials in environment.")

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    results = sp.search(q=search_query, type='track', limit=3)
    items = results.get('tracks', {}).get('items', [])
    
    if not items:
        return None 

    print("select the track that you requested(0 to 2)...")

    for index, track in enumerate(items):
        artist_name = track.get('artists', [{'name' : 'Unknown'}])[0]['name']
        track_name = track.get('name', 'Unknown Name')
        print(f"[{index}] - {track_name} by {artist_name}")

    while True :
        user_input = input(f"select the music that you want to review (0 to {len(items)-1})")

        try:
            x = int(user_input)

            if 0 <= x < len(items):
                selected_track = items[x]
                break
            else:
                print("number out of range, try again.")

        except ValueError:
            print("invalid input")

    metadata = {
        "name": selected_track.get('name', 'Unknown Name'),
        "artist": selected_track.get('artists', [{'name': 'Unknown'}])[0]['name'],
        "release_date": selected_track.get('album', {}).get('release_date', 'Unknown Date'),
        "preview_url": selected_track.get('preview_url') 
    }
    
    return metadata