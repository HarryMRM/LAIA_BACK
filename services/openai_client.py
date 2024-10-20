#Primero se importa la libreria openai la cual proporciona acceso a las funcionalidades de OPENIA.
#Despues se importa la clase path que ayuda con las rutas de archivos entre sistemas operativos.
#Se importa OPENAI_API_KEY la cual permite autentificar las solicitudes de OPENAI.
import openai
from pathlib import Path
from config import OPENAI_API_KEY
from utils.json_utils import ask
from utils.pandas_utils import load_embeddings
openai.api_key = OPENAI_API_KEY
embeddings_path = "data/uabcEmb.csv"

#Se define la llamada que va a recibir el texto a convertir en audio como parametro.
#Despues se crea un cliente para realizar solicitudes a la API de OpenIA.
#Posteriormente se define la ruta del archivo donde se guardara la conversión a voz del texto
# Se realiza la llamada para crear el audio mediante OPENAI, se selecciona el modelo de voz,
# la tonalidad de la misma y el texto que se utilizará.
# Finalmente se guarda en la ruta el archivo de voz y la retorna para su uso posterior. 
def generate_speech(input_text):
    client = openai.OpenAI()
    speech_file_path = Path('audio/speech-result.mp3')
    response = client.audio.speech.create(
        model='tts-1-hd',
        voice="nova",
        input=input_text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

def generate_response(input_text):
    client = openai.OpenAI()
    df = load_embeddings(embeddings_path)
    answer = ask(input_text, df, client, "text-embedding-ada-002", "gpt-4o-mini")
    return answer