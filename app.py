from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import openai
import os
import warnings
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)
os.environ["OPENAI_API_KEY"] = 'a'
warnings.filterwarnings("ignore", category=DeprecationWarning)

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        if 'input_text' not in data:
            return jsonify({"error": "Input text not provided"}), 400
        input_text = data['input_text']
        openai.api_key = os.getenv("OPENAI_API_KEY")
        client = openai.OpenAI()
        speech_file_path = Path('speech-result.mp3')
        response = client.audio.speech.create(
            model='tts-1-hd',
            voice="nova",
            input=input_text
        )
        response.stream_to_file(speech_file_path)
        audio_content = BytesIO(response.content)
        archivo_base64 = base64.b64encode(audio_content.getvalue()).decode('utf-8')
        return jsonify({
            "input_text": input_text,
            "audio_path": request.url_root + 'speech-result.mp3',
            "audio_file": archivo_base64
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)