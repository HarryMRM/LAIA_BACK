from flask import Blueprint, request, jsonify
from services.openai_client import generate_speech
from utils.file_utils import convert_file_to_base64
text_to_speech_route = Blueprint('text_to_speech', __name__)

@text_to_speech_route.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        if 'input_text' not in data:
            return jsonify({"error": "Input text not provided"}), 400
        input_text = data['input_text']
        speech_file_path = generate_speech(input_text)
        audio_base64 = convert_file_to_base64(speech_file_path)
        return jsonify({
            "input_text": input_text,
            "audio_path": request.url_root + 'speech-result.mp3',
            "audio_file": audio_base64
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
