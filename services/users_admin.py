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
Se define una función la cual se encarga de validar si un usuario ya existe en la base de datos
"""
def user_exists(doc):
  try:
    user = collection.find_one({"user": doc.get("user")})
    
    if ('_id' in user):
      return True #If the user does exist
    else:
      return False #If the user doesn't exists
  
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al insertar el documento: {connectionError}")


"""
Se define una función la cual se encarga de insertar un documento en la colección
Recibe un diccionario con los datos a insertar
Retorna el objeto insertado
"""
def insertDocument(doc):
  try:
    if not user_exists(doc): #If the user doesn't exist
      resp = collection.insert_one(doc)
      
      inserted = collection.find_one({"_id": resp.inserted_id})
      inserted["_id"] = str(inserted.get("_id"))
      
      return inserted
    
    else: #If the user do exists
      return {"error": "User already exists"}
    
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al insertar el documento: {connectionError}")


"""
Se define una función la cual se encarga de leer todos los documentos de la colección
No recibe parámetros
Retorna una lista con los objetos presentes en la base de datos
"""
def validate_user(doc):
  try:
  
    user = collection.find_one({"user": doc.get("user")})
    
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