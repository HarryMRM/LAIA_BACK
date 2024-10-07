import openai
from pathlib import Path
from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

def generate_speech(input_text):
    client = openai.OpenAI()
    speech_file_path = Path('speech-result.mp3')
    response = client.audio.speech.create(
        model='tts-1-hd',
        voice="nova",
        input=input_text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path
