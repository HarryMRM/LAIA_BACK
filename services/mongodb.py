"""Primero se importa la pymongo openai la cual proporciona acceso a las funcionalidades de MongoDB.
Se importan MONGO_URI, MONGO_DATABASE, y MONGO_COLLECTION las cuales permiten autentificar las solicitudes a MongoDB."""
import pymongo
from config import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

""" Se establece un tiempo de espera límite de 1000 milisegundos (1 segundo) para la conexión con la base de datos """
TIMEOUT = 1000

"""
Se define una función la cual se encarga de conectar con el cliente de la base de datos
No recibe parámetros
Retorna la conexión con el cliente
"""
# def connectClient():
try:
  cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS = TIMEOUT)
  print("Conexión con la base de datos establecida!")
  # return cliente

except pymongo.errors.ServerSelectionTimeoutError as timeError:
  print(f"Tiempo excedido: {timeError}")
  
except pymongo.errors.OperationFailure as operationError:
  print(f"Error de operación: {operationError}")


"""
Se define una función la cual se encarga de conectar con la colección de la base de datos
Recibe la conexión con el cliente
Retorna la conexión con la colección
"""
# def connectCollection(cliente):
try:
  db = cliente[MONGO_DATABASE]
  collection = db[MONGO_COLLECTION]
  # return collection
  
except pymongo.errors.CollectionInvalid as collectionError:
  print(f"Error al conectar con la colección: {collectionError}")


"""
Se define una función la cual se encarga de cerrar la conexión con el cliente de la base de datos
Recibe la conexión con el cliente
No tiene retorno
"""
# def closeClient(cliente):
#   try:
#     cliente.close()
#   except Exception as error:
#     print(f"Error al cerrar la conexión: {error}")


"""
Se define una función la cual se encarga de insertar un documento en la colección
Recibe un diccionario con los datos a insertar
Retorna el objeto insertado
"""
def insertDocument(doc):
  try:
    resp = collection.insert_one(doc)
    
    inserted = collection.find_one({"_id": resp.inserted_id})
    inserted["_id"] = str(inserted.get("_id"))
    
    return inserted
    
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al insertar el documento: {connectionError}")


"""
Se define una función la cual se encarga de leer todos los documentos de la colección
No recibe parámetros
Retorna una lista con los objetos presentes en la base de datos
"""
def readDocuments():
  try:
    documents = list(collection.find().sort("createdAt", pymongo.ASCENDING))
    for document in documents:
      document["_id"] = str(document.get("_id"))
    
    return documents
  
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al leer los documentos: {connectionError}")


"""
Se define una función la cual se encarga de eliminar todos los documentos de la colección
No recibe parámetros
No tiene retorno
"""
def deleteAllDocuments():
  try:
    deleteResult = collection.delete_many(filter={})
    return deleteResult.deleted_count
    
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al borrar el documento: {connectionError}")