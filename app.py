"""Se importan las respectivas clases 
Primero se importa la clase Flask para poder trabajar en python utilizando Flask.
Posteriormente se utiliza cors el cual permite trabajar con el mismo, otorgando permisos de acceso para la aplicación segun sea necesario.
Finalmente la clase text_to_speech la cual se encarga de convertir el texto en audio."""

from flask import Flask
from flask_cors import CORS
from routes.response_ai import response_ai_route
from routes.response_mongodb import response_mongodb_route
from routes.users_admin import users_admin  # Importa el nuevo módulo de rutas

"""Se crea la aplicación flask y se habilita CORS para otorgar los permisos necesarios que sean requeridos por
los dominios del front end. 

Se registra un blueprint para estructurar las operaciones relacionadas a la conversión texto a voz a ejecutar
en la aplicación desde text_to_speech.
Se registra un blueprint para estructurar las operaciones relacionadas a la gestión de la base de datos a ejecutar
en la aplicación desde database.

Se verifica que el archivo este siendo ejecutado directamente y en caso de cumplirse tal condición,
se corre la aplicación flask en modo depuración, permitiendo constante actualización durante su ejecución."""

app = Flask(__name__)
CORS(app)
app.register_blueprint(response_ai_route)
app.register_blueprint(response_mongodb_route)
app.register_blueprint(users_admin)

if __name__ == '__main__':
    app.run(debug=True)
