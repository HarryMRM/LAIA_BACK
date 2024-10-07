#Se importa blueprint para organizar el código, accede a los datos http y los convierte en formato JSON.
#Se importa la función para convertir audio en texto mediante openai y la función para dar formato base64 a los archivos.
from flask import Blueprint, request, jsonify
from services.openai_client import generate_speech
from utils.file_utils import convert_file_to_base64
text_to_speech_route = Blueprint('text_to_speech', __name__)

#Se crea un blueprint para las rutas de texto y voz.
# se define la ruta que acepta solo solicitudes POST.
# Se obtiene el contenido JSON de la solicitud la cual deberia contener "input_text".
# Posteriormente se verifica que este presente,  si no esta presente enviara un mensaje de error,
# de caso contrario, se extrae el texto y se llama la función para generar el audio a partir del mismo.
# El archivo de audio se pasa a formato base64 y una vez terminado el proceso.
# Se crea y retorna JSON, el texto, la ruta del archivo de audio y la version Base64.
# Se utiliza except en caso de que ocurra un error dentro de try, regresando un mensaje de error en formato JSON,
# junto con el codigo 500, error interno del servidor. 
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
