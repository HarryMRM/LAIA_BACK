from cryptography.fernet import Fernet # type: ignore
from config import CRYPTING_KEY

"""
Se define un objeto de la clase Fernet
el cual se encarga de encriptar y desencriptar la información
"""
encrypter = Fernet(CRYPTING_KEY)


# """
# Se define una función la cual se encarga de convertir la información encriptada en String
# """
# def encrypt_to_string(encrypted_data):
#     return str(encrypted_data.strip().replace("b'", "").replace("'", ""))


# """
# Se define una función la cual se encarga de convertir la información no criptada en bytes
# """
# def encrypt_to_string(encrypted_data):
#     return encrypted_data.strip().replace("b'", "").replace("'", "").encode()


"""
Se define una función la cual se encarga de encriptar la información
"""
def encrypt_data(data):
    # print(f"encrypt_data: {type(data)}-{data}")
    return encrypter.encrypt(data.encode())


"""
Se define una función la cual se encarga de desencriptar la información
"""
def decrypt_data(encrypted_data):
    # print(f"decrypt_data: {type(encrypted_data)}-{encrypted_data}")
    return encrypter.decrypt(encrypted_data).decode()


"""
Se define una función la cual se encarga de comparar
la información encriptada con la información no encriptada
Retorna True si son iguales, False en caso contrario
"""
def data_equals_encrypted(data, encrypted_data):
    # print(f"data_equals_encrypted: {type(data)}-{data} - {type(encrypted_data)}-{encrypted_data}")
    return data == decrypt_data(encrypted_data)
