import pymongo
from config import MONGO_URI, MONGO_DATABASE_USR, MONGO_COLLECTION_TKN
from utils.token_generator import (
    create_access_token,
    create_refresh_token,
    verify_access_token,
    verify_refresh_token,
)


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
        collection.insert_one({"token": refresh_token})
        return refresh_token

    except pymongo.errors.ConnectionFailure as connectionError:
        print(f"Error al insertar el documento: {connectionError}")
        return None


"""
Se define una función la cual se encarga de obtener un nuevo token de acceso
"""


def get_new_access_token(refresh_token):
    try:
        encontrado = collection.find_one({"token": refresh_token})
        if encontrado:
            payload = verify_refresh_token(encontrado.get("token"))
            if payload:
                return create_access_token(payload.get("user"))
            else:
                return None
        else:
            return None

    except pymongo.errors.ConnectionFailure as connectionError:
        print(f"Error al insertar el documento: {connectionError}")
        return None


"""
Se define una función la cual se encarga de obtener el token del header
"""


def get_token_from_headers(headers):
    if (headers) and ("Authorization" in headers):
        parted = headers["Authorization"].split(" ")
        if len(parted) == 2:
            return parted[1]
        else:
            return None
    else:
        return None
