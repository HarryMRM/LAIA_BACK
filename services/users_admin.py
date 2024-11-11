"""Primero se importa la pymongo openai la cual proporciona acceso a las funcionalidades de MongoDB.
Se importan MONGO_URI, MONGO_DATABASE_USR, y MONGO_COLLECTION_USR las cuales permiten autentificar las solicitudes a MongoDB."""
import pymongo
from config import MONGO_URI, MONGO_DATABASE_USR, MONGO_COLLECTION_USR

""" Se establece un tiempo de espera límite de 1000 milisegundos (1 segundo) para la conexión con la base de datos """
TIMEOUT = 1000

"""
Se conecta con el cliente de la base de datos
"""
try:
  cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS = TIMEOUT)
  print("Conexión con la base de datos establecida!")

except pymongo.errors.ServerSelectionTimeoutError as timeError:
  print(f"Tiempo excedido: {timeError}")
  
except pymongo.errors.OperationFailure as operationError:
  print(f"Error de operación: {operationError}")


"""
Se conecta el cliente con la colección de la base de datos
"""
try:
  db = cliente[MONGO_DATABASE_USR]
  collection = db[MONGO_COLLECTION_USR]
  
except pymongo.errors.CollectionInvalid as collectionError:
  print(f"Error al conectar con la colección: {collectionError}")


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