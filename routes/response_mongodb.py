"""Se importa blueprint para organizar el código, accede a los datos http y los convierte en formato JSON.
Se importan las funciones para insertar un documento el la base de datos, leer todos los documentos de la base de datos,
y eliminar todos los documentos  de la base de datos."""
from flask import Blueprint, request, jsonify
from services.mongodb import insertDocument, readDocuments, deleteAllDocuments
response_mongodb_route = Blueprint('messages_database', __name__)

"""
Se crea un blueprint para las rutas de la base de datos.
Se define la ruta que acepta solo solicitudes POST para la base de datos.
Se obtiene el contenido JSON de la solicitud la cual deberia contener "userID", "message" y "photoUrl".
Posteriormente se verifica que estos esten presentes, si no estan presentes enviara un mensaje de error de petición,
en caso contrario, se extraen los datos y se llama la función para insertar un documento en la base de datos.
La función de insersión recibe un diccionario con los datos a insertar y retorna el objeto insertado.
Se retorna un JSON con el documento insertado y el codigo 200, que indica que la solicitud fue exitosa.
Se utiliza except en caso de que ocurra un error dentro de try, regresando un mensaje de error en formato JSON,
junto con el codigo 500, error interno del servidor.
"""
@response_mongodb_route.route('/api/messages_database', methods=['POST'])
def insert_message():
  try:
    data = request.get_json()
    
    if ('userID' not in data) or ('message' not in data) or ('photoUrl' not in data):
      return jsonify({"error": "You may need to add a userID, message or photoUrl."}), 400
    
    document = {
      "userID": data.get('userID'),
      "message": data.get('message'),
      "photoUrl": data.get('photoUrl'),
    }
    inserted = insertDocument(document)
    return jsonify(inserted), 200
  
  except Exception as e:
    return jsonify({"error inserting": str(e)}), 500


"""
Se crea un blueprint para las rutas de la base de datos.
Se define la ruta que acepta solo solicitudes GET para la base de datos.
No se espera recibir nada, por lo que no se hace una validación.
Posteriormente se llama la función para obtener todos los documentos en la base de datos.
La función de obtención retorna una lista con los objetos presentes en la base de datos.
Se retorna un JSON con la lista de elementos y el codigo 200, que indica que la solicitud fue exitosa.
Se utiliza except en caso de que ocurra un error dentro de try, regresando un mensaje de error en formato JSON,
junto con el codigo 500, error interno del servidor.
"""
@response_mongodb_route.route('/api/messages_database', methods=['GET'])
def get_messages():
  try:
    messages = readDocuments()
    return jsonify(messages), 200
  
  except Exception as e:
    return jsonify({"error reading": str(e)}), 500


"""
Se crea un blueprint para las rutas de la base de datos.
Se define la ruta que acepta solo solicitudes DELETE para la base de datos.
No se espera recibir nada, por lo que no se hace una validación.
Posteriormente se llama la función para eliminar todos los documentos en la base de datos.
La función de eliminación no retorna nada.
Se retorna un JSON con un objeto con el atributo "mensaje" indicando la operación exitora,
y el codigo 200, que indica que la solicitud fue exitosa.
Se utiliza except en caso de que ocurra un error dentro de try, regresando un mensaje de error en formato JSON,
junto con el codigo 500, error interno del servidor.
"""
@response_mongodb_route.route('/api/messages_database', methods=['DELETE'])
def delete_messages():
  try:
    deleteAllDocuments()
    return jsonify({"message": "All messages deleted successfully"}), 200
  
  except Exception as e:
    return jsonify({"error deleting": str(e)}), 500