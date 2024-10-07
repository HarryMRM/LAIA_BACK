#Se importa la libreria os la cual permite acceder a variables de entorno.
#Posteriormente se importa warnings la cual presenta advertencias de python para uso en la aplicación.
#Y finalmente load_dotenv la cual permite que las variables de entorno sean cargadas en entorno local para ponerlas en el código.
import os
import warnings
from dotenv import load_dotenv

#Se cargan las variables de entorno mediante load_dotenv
#Mediante la función os.getenv se accede a la variable de entorno
#OPENAI_API_KEY la cual permite autenticar las peticiones realizadas de la API de OPENAI
#Despues se ignoran las advertencias de tipo: DeprecationWarning.
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
warnings.filterwarnings("ignore", category=DeprecationWarning)
