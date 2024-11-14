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
  print("Conexión con la base de datos de usuarios establecida!")

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
def user_exists(user):
  try:
    user_data = collection.find_one({"user": user})

    if (user_data != None):
      return True #If the user exists
    else:
      return False #If the user not exists
  
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al insertar el documento: {connectionError}")


"""
Se define una función la cual valida la contraseña de un usuario
"""
def correct_password(user, password):
  try:
    user_data = collection.find_one({"user": user})
    
    if (user_data.get("password") == password):
      return True #If the password is correct
    else:
      return False #If the password is not correct
  
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al insertar el documento: {connectionError}")


"""
Se define una función la cual se encarga de insertar el registro de un usuario en la base de datos
Recibe un diccionario con los datos a insertar
Retorna el usuario insertado o un mensaje de error
"""
def create_user(doc):
  try:
    if not user_exists(doc.get("user")): #If the user not exists
      resp = collection.insert_one(doc)
      
      inserted = collection.find_one({"_id": resp.inserted_id})
      inserted["_id"] = str(inserted.get("_id"))
      
      return inserted
    
    else: #If the user exists
      return {"error": "El usuario ya existe"}
    
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al insertar el documento: {connectionError}")


"""
Se define una función la cual se encarga de lautenticar el usuario y contraseña
Reibe un diccionario con usuario y contraseña
Retorna un mensaje indicando éxito o error
"""
def validate_user(doc):
  try:
    if user_exists(doc.get("user")): #If the user exists
      
      if correct_password(doc.get("user"), doc.get("password")): #If the password is correct
        return {"message": "Usuario validado"}
      
      else:
        return {"error": "Contraseña incorrecta"}
    
    else:
      return {"error": "Usuario no encontrado"}
  
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al leer los documentos: {connectionError}")


"""
Se define una función la cual se encarga de actualizar los datos de un usuario en la base de datos
Recibe un diccionario con los datos a actualizar y los datos nuevos
Retorna un diccionario con el usuario actualizado o un mensaje de error
"""
def update_user(doc):
  try:
    if user_exists(doc.get("user")):
      if "new_password" in doc:
        if True: #Validar codigo de confirmación
          if doc.get("new_password") != doc.get("password"):
            #Update the password
            updated = collection.update_one(
              filter={"user": doc.get("user")},
              update={"$set": {"password": doc.get("new_password")}}
            )
            updated = collection.find_one({"user": doc.get("user")})
            updated["_id"] = str(updated.get("_id"))
            return updated
          
          else:
            return {"error": "La nueva contraseña no puede ser igual a la actual"}
        
        else:
          return {"error": "Código de confirmación incorrecto"}
      
      elif "new_user" in doc:
        if doc.get("new_user") != doc.get("user"):
          if not user_exists(doc.get("new_user")):
            #Update the user
            updated = collection.update_one(
              filter={"user": doc.get("user")},
              update={"$set": {"user": doc.get("new_user")}}
            )
            updated = collection.find_one({"user": doc.get("new_user")})
            updated["_id"] = str(updated.get("_id"))
            return updated
          
          else:
            return {"error": "El usuario ya existe"}
        
        else:
          return {"error": "El nuevo usuario no puede ser el mismo que el actual"}
        
      else:
        return {"error": "No se especificaron datos a actualizar"}
    
    else:
      return {"error": "Usuario no encontrado"}
    
  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al borrar el documento: {connectionError}")


"""
Se define una función la cual se encarga de eliminar un usuario de la base de datos
Recibe un diccionario con el usuario a eliminar
Retorna un mensaje indicando éxito o error
"""
def delete_user(doc):
  try:
    if user_exists(doc.get("user")):
      if correct_password(doc.get("user"), doc.get("password")):
        deleted = collection.find_one({"user": doc.get("user")})
        deleted["_id"] = str(deleted.get("_id"))

        collection.delete_one({"user": doc.get("user")})
        print(f"Usuario eliminado: {deleted}")
        return deleted

      else:
        return {"error": "Contraseña incorrecta"}

    else:
      return {"error": "Usuario no encontrado"}

  except pymongo.errors.ConnectionFailure as connectionError:
    print(f"Error al borrar el documento: {connectionError}")