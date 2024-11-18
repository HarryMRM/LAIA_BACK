import jwt # type: ignore
import datetime

"""
Se define una función la cual se encarga de crear una firma jwt
Recibe una carga útil
Retorna un token o un error
"""
def sign(payload, is_access_token): #secret es la clave secreta
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=10)  # Token expira en 10 segundos
    return jwt.encode({"some": payload, "exp": expiration},
                      "access" if is_access_token else "refresh",
                      algorithm="HS256")


"""
Se define una función la cual se encarga de crear una firma jwt
Recibe el token a decodificar
Retorna la carga tokenizada o un error de expiración
"""
def decode(encoded_jwt, is_access_token): #secret es la clave secreta
    try:
        return jwt.decode(encoded_jwt,
                          "access" if is_access_token else "refresh",
                          algorithms=["HS256"])
    
    except jwt.ExpiredSignatureError:
        return "Token has expired"


"""
Se define una función la cual se encarga de crear un token de acceso
Recibe 
Retorna un token o un error
"""
def create_access_token(doc):
    return sign(doc, True)

"""
Se define una función la cual se encarga de crear un token de recarga
Recibe 
Retorna un token o un error
"""
def create_refresh_token(doc):
    return sign(doc, False)