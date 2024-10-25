"""Se importa la libreria os la cual permite acceder a variables de entorno.
Posteriormente se importa warnings la cual presenta advertencias de python para uso en la aplicación.
Y finalmente load_dotenv la cual permite que las variables de entorno sean cargadas en entorno local para ponerlas en el código."""
import os
import warnings
from dotenv import load_dotenv

"""Se cargan las variables de entorno mediante load_dotenv
Mediante la función os.getenv se accede a la variable de entorno
OPENAI_API_KEY la cual permite autenticar las peticiones realizadas de la API de OPENAI
MONGO_URI la cual contiene la url para establecer conexión con la base de datos
MONGO_DATABASE la cual contiene el nombre de la base de datos
MONGO_COLLECTION la cual contiene el nombre de la colección en la base de datos
Despues se ignoran las advertencias de tipo: DeprecationWarning."""
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

warnings.filterwarnings("ignore", category=DeprecationWarning)
