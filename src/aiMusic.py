import ollama

def getMood():
    print("Hey, how are you feeling? (sad, happy, angry...)")
    mood = input(" ")
    return mood

def getType():
    print("and what type of music fo you want to hear today? (rap, rock, pop...)")
    type = input(" ")
    return type

def suggestOne(taste, mood, type):

    prompt = f"""
    You are a friend of user and an expert music curator.
    The user wants you to reccomend a music based on his music taste: {taste}, in his current mood: {mood} and in what type of music he wants to hear: {type}.
    Reccomend to user EXACTLY 1 music considerating users taste, but changing tempo and genre based on the user's mood and on what he wants to hear.
    """

    try:
        print(f"analyzing user mood and music taste to reccomend a music...")

        response = ollama.chat(model = 'llama3', messages=[{'role': 'user', 'content': prompt}])

        return response['message']['content']
    except Exception as e:
        print(f"AI error : {e}")
        return None
    
def genPlaylist(taste, mood, type):

    prompt = f"""
    You are a friend of user and a expert music curator.
    Create a playlist to the user of EXACTLY 30 tracks based on his taste: {taste}, mood: {mood}, and the music type that he wants to hear: {type}.

    CRITICAL INSTRUCTION: 
Try to find songs that are NOT already in their taste history. Push the user to discover new artists and tracks, but ensure the tempo and genre perfectly match their mood and type inputs.

    Format your response strictly as a markdown table with the following columns: | # | Song Name | Artist | Tempo | Genre |
"""
    
    try:
        print("evaluating user inputs and creating the playlist...")
        response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])

        return response['message']['content']
    except Exception as e:
        print(f"AI error: {e}")
        return None