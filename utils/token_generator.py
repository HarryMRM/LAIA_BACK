import jwt  # type: ignore
import datetime

"""
Se define una función la cual se encarga de crear una firma jwt
Recibe una carga útil
Retorna un token o un error
"""


def sign(payload, is_access_token):  # secret es la clave secreta
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        seconds=3600
    )  # Token expira en 3600 segundos (60 minutos o 1 hora)
    return jwt.encode(
        {"some": payload, "exp": expiration},
        "access" if is_access_token else "refresh",
        algorithm="HS256",
    )


"""
Se define una función la cual se encarga de crear una firma jwt
Recibe el token a decodificar
Retorna la carga tokenizada o un error de expiración
"""


def decode(encoded_jwt, is_access_token):  # secret es la clave secreta
    try:
        return jwt.decode(
            encoded_jwt,
            "access" if is_access_token else "refresh",
            algorithms=["HS256"],
        )

    except jwt.ExpiredSignatureError:
        return None


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


"""
Se define una función la cual se encarga de verificar un token de acceso
"""


def verify_access_token(token):
    return decode(token, True)


"""
Se define una función la cual se encarga de verificar un token de recarga
"""


def verify_refresh_token(token):
    return decode(token, False)
