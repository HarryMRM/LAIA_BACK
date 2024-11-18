import pymongo
from config import MONGO_URI, MONGO_DATABASE_USR, MONGO_COLLECTION_TKN
from utils.token_generator import create_access_token, create_refresh_token


""" Se establece un tiempo de espera límite de 1000 milisegundos (1 segundo) para la conexión con la base de datos """
TIMEOUT = 1000

"""
Se conecta con el cliente de la base de datos
"""
try:
    cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=TIMEOUT)
    print("Conexión con la base de datos de tokens establecida!")

except pymongo.errors.ServerSelectionTimeoutError as timeError:
    print(f"Tiempo excedido: {timeError}")

except pymongo.errors.OperationFailure as operationError:
    print(f"Error de operación: {operationError}")


"""
Se conecta el cliente con la colección de la base de datos
"""
try:
    db = cliente[MONGO_DATABASE_USR]
    collection = db[MONGO_COLLECTION_TKN]

except pymongo.errors.CollectionInvalid as collectionError:
    print(f"Error al conectar con la colección: {collectionError}")


"""
Se define una función la cual se encarga de crear un token de acceso
"""


def get_access_token(doc):
    return create_access_token(doc)


"""
Se define una función la cual se encarga de crear un token de recarga
"""


def get_refresh_token(doc):
    try:
        refresh_token = create_refresh_token(doc)
        collection.insert_one({"refresh_token": refresh_token})
        return refresh_token

    except pymongo.errors.ConnectionFailure as connectionError:
        print(f"Error al insertar el documento: {connectionError}")
        return False
