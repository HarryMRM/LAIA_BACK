import os
import requests
from pathlib import Path
from config import NARAKEET_API_KEY
narakeet_api_key = NARAKEET_API_KEY

def generate_speech(input_text):
    url = 'https://api.narakeet.com/text-to-speech/mp3?voice=silvana'
    options = {
        'headers': {
            'Accept': 'application/octet-stream',
            'Content-Type': 'text/plain',
            'x-api-key': narakeet_api_key,
        },
        'data': input_text.encode('utf8')
    }
    os.makedirs('audio', exist_ok=True)
    speech_file_path = Path('audio/speech-result.mp3')
    if os.path.exists(speech_file_path):
        os.remove(speech_file_path)
    with open(speech_file_path, 'wb') as f:
        f.write(requests.post(url, **options).content)
    return speech_file_path
