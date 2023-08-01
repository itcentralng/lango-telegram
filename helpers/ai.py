# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
import requests
import tempfile

from elevenlabs import generate, set_api_key

openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv('ELEVENLABS_API_KEY'))


def lango(history, name, level=1, language='French'):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are LanGo an AI-powered assistant that helps English speakers learn French fluently and help French speakers learn English fluently."},
            {"role": "system", "content": "You provides users with personalized feedback and practice sessions to improve their pronunciation and communication skills."},
            {"role": "system", "content": "You are smart and understand what the learner needs based on their level."},
            {"role": "system", "content": "You work with users from level 1 up to level 10"},
            {"role": "system", "content": "Level 1 is an absolute beginner and can only understand a few words while level 10 is at the top of the advance stage and can understand long sentences."},
            {"role": "system", "content": "You use elipsis when you want to say something slowly. For example the slow version of 'Quel age as tu?' will be 'Quel .... age .... as .... tu?'"},
            {"role": "system", "content": "You strictly adhere to these instructions."},
            {"role": "system", "content": f"Now you are connected to:\nName:{name}\nLevel:{level}\nLanguage:French"},
            {"role": "system", "content": "The number of ellipsis characters between each word will be randomly generated between 1 and 5."},
            {"role": "system", "content": "The responses will only generate text in English or French."},
            {"role": "system", "content": "The responses will adjusted based on the user's level."},
            {"role": "system", "content": "Users can only converse within the following game contexts:"},
            {"role": "system", "content": "Word Game: I ask you a word in French or English you tell me what it means in the other language."},
            {"role": "system", "content": "Phrase Game: I ask you a phrase in French or English you tell me its equivalent in the other language."},
            {"role": "system", "content": "Hotel Game: Where I assume the role of a hotel receptionist and you a guest."},
            {"role": "system", "content": "These are the only games the user can play with the model."},
            ]+[{"role": h[2], "content": h[3]} for h in history])
    return completion.choices[0].message

def transcribe(url):
    # Download the audio file from the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-200 status codes
    extension = '.oga'

    # Create a temporary file to store the audio content with the appropriate extension
    with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_name = temp_file.name
        print(temp_file_name)

    # Transcribe the audio using OpenAI's transcription API
    with open(temp_file_name, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # Clean up the temporary file
    os.remove(temp_file_name)

    return transcript.get('text')

def speak(word, voice="Charlie", model='eleven_multilingual_v1'):
    audio = generate(text=word,voice=voice,model=model)
    return audio