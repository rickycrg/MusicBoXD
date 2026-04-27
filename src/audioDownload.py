import yt_dlp
import os
import glob


def downloadAudio(youtubeUrl):
    print("starting the download...")

    for old_file in glob.glob("temp_audio.*"):
        try:
            os.remove(old_file)
        except OSError:
            pass

    ydlOpts={
        'format' : 'm4a/bestaudio/best',
        'postprocessors':[{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'wav',
        }],
        'outtmpl' : 'temp_audio.%(ext)s',
        'extractor_args': {
            'youtube': ['client=android']
        },
        'quiet' : True,
        'noplaylist' : True
    }

    try:
        with yt_dlp.YoutubeDL(ydlOpts) as ydl:
            ydl.download([youtubeUrl])

        downloadedFiles = glob.glob("temp_audio.*")
        
        actualFile = downloadedFiles[0]

        if downloadedFiles:
            print("successfully downloaded.")
        else:
            print("downloaded but not complete.")

        return actualFile
    except Exception as e:
        print(f"error : {e}")
        return None