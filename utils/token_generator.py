import jwt


"""
Se define una función la cual se encarga de crear una firma jwt
Recibe 
Retorna un token o un error
"""
def sign(doc):
    return jwt.encode({"some": "payload"}, "secret", algorithm="HS256")


"""
Se define una función la cual se encarga de crear una firma jwt
Recibe 
Retorna un token o un error
"""
def decode(encoded_jwt):
    return jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])



"""
Se define una función la cual se encarga de crear un token de acceso
Recibe 
Retorna un token o un error
"""
def create_access_token(doc):
    pass

"""
Se define una función la cual se encarga de crear un token de recarga
Recibe 
Retorna un token o un error
"""
def create_refresh_token(doc):
    pass