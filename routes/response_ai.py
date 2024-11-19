"""Se importa blueprint para organizar el código, accede a los datos http y los convierte en formato JSON.
Se importa la función para convertir audio en texto mediante openai y la función para dar formato base64 a los archivos."""
from flask import Blueprint, request, jsonify
from services.openai_client import generate_speech as openai_speech, generate_response as openai_response
from services.narakeet_client import generate_speech as narakeet_speech
from utils.file_utils import convert_file_to_base64
from utils.string_utils import convert_text
response_ai_route = Blueprint('text_to_speech', __name__)

"""Se crea un blueprint para las rutas de texto y voz.
se define la ruta que acepta solo solicitudes POST.
Se obtiene el contenido JSON de la solicitud la cual deberia contener "input_text".
Posteriormente se verifica que este presente,  si no esta presente enviara un mensaje de error,
de caso contrario, se extrae el texto y se llama la función para generar el audio a partir del mismo.
El archivo de audio se pasa a formato base64 y una vez terminado el proceso.
Se crea y retorna JSON, el texto, la ruta del archivo de audio y la version Base64.
Se utiliza except en caso de que ocurra un error dentro de try, regresando un mensaje de error en formato JSON,
junto con el codigo 500, error interno del servidor. """
@response_ai_route.route('/api/text-to-speech', methods=['POST'])
def response_ai():
    try:
        data = request.get_json()

        # Validar entrada
        if 'input_text' not in data:
            return jsonify({"error": "Input text not provided"}), 400
        if 'ia_model' not in data or 'ia_model' not in data:
            return jsonify({"error": "Missing model selectors"}), 400
        if 'voice_model' not in data or 'ia_model' not in data:
            return jsonify({"error": "Missing model selectors"}), 400
        
        input_text = data['input_text']
        voice_model = data['voice_model']
        ia_model = data['ia_model']

        # Generar respuesta de IA según el modelo seleccionado
        if ia_model == "openai":
            response_text = openai_response(input_text)
        elif ia_model == "ollama":
            response_text = openai_response(input_text)
        else:
            return jsonify({"error": f"Unsupported IA model: {ia_model}"}), 400

        response_text_fix = convert_text(response_text)

        # Generar audio según el modelo de voz seleccionado
        if voice_model == "narakeet":
            speech_file_path = narakeet_speech(response_text_fix)
        elif voice_model == "openai":
            speech_file_path = openai_speech(response_text_fix)
        elif voice_model == "none":
            # Sin voz, devolver solo texto
            return jsonify({
                "input_text": response_text,
                "audio_path": None,
                "audio_file": None
            }), 200
        else:
            return jsonify({"error": f"Unsupported voice model: {voice_model}"}), 400

        # Convertir archivo de audio a base64
        audio_base64 = convert_file_to_base64(speech_file_path)

        return jsonify({
            "input_text": response_text,
            "audio_path": request.url_root + 'speech-result.mp3',
            "audio_file": audio_base64
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500