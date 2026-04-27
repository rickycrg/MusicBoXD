
import librosa
import numpy as np

def getBpmFromFile(filepath):
    print("analyzing audio...")
    try:
        y, sr = librosa.load(filepath, duration=30.0)

        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)

        return round(bpm, 1)
    
    except Exception as e:
        print(f"error in bpm calculation : {e}")
        return None
