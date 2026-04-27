# src/youtube_fetcher.py
import os
from googleapiclient.discovery import build

from dotenv import load_dotenv

def get_youtube_url(song_name, artist):
    """
    Searches YouTube for the song and returns the direct video URL.
    """

    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    if not api_key:
        raise ValueError("Missing YouTube API key in environment.")

    # Build the YouTube service
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Craft a highly specific search query to avoid covers/live versions
    search_query = f"{song_name} {artist} official audio"

    # Execute the search
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=search_query,
        type="video"
    )
    
    # .execute() makes the actual network call to Google's servers
    response = request.execute()

    items = response.get('items', [])
    if not items:
        return None

    # Extract the unique Video ID and build the standard YouTube link
    video_id = items[0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    return video_url