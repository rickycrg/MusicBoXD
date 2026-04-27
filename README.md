**MusicBoXD 🎵** is an application to give opinions about Songs and Albums, and based on the user opinion, give new personalized Raccomendation lists based on what the user want, making easier to find new tracks to hear and discover new types of songs.

    - Smart Recommendations: Suggests single tracks based on your historical preferences and current mood.

    - Custom Playlists: Generates 30-song playlists tailored to specific genres, tempos, and emotional states.

    - Discovery Engine: Actively pushes you to discover new artists while respecting your underlying musical taste.

**How it works ⚙️**

    Consists of a python application integrated with the AI model Llama3 (via Ollama).
    User data (opinions) are saved in a CSV file using pandas library. The AI model analyze your musical taste and reccomends new music- or makes a custom playlist, based on your mood and on requested genres.

*New functionalities and improvements coming soon...*

**(BYOK)⚒️**

Setup and Installation.

To run MusicBoXD locally, you need to export the following variables (Spotify and YouTube credentials) in the terminal before using the app:

    export SPOTIPY_CLIENT_ID="your-client-id"
    export SPOTIPY_CLIENT_SECRET="your-secret"
    export YOUTUBE_API_KEY="your-youtube-api-key"

After keys exportation, ensure you have Python installed and install the required dependencies in the terminal:

    pip install -r requirements.txt