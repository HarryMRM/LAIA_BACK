import resend  # type: ignore
import pymongo
import random
from config import RESEND_API_KEY, MONGO_URI, MONGO_DATABASE_USR, MONGO_COLLECTION_PWD

resend.api_key = RESEND_API_KEY

CODE_LENGTH = 8
CODE_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


""" Se establece un tiempo de espera límite de 1000 milisegundos (1 segundo) para la conexión con la base de datos """
TIMEOUT = 1000

"""
Se conecta con el cliente de la base de datos
"""
try:
    cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=TIMEOUT)
    print("Conexión con la base de datos de recuperación establecida!")

except pymongo.errors.ServerSelectionTimeoutError as timeError:
    print(f"Tiempo excedido: {timeError}")

except pymongo.errors.OperationFailure as operationError:
    print(f"Error de operación: {operationError}")


"""
Se conecta el cliente con la colección de la base de datos
"""
try:
    db = cliente[MONGO_DATABASE_USR]
    collection = db[MONGO_COLLECTION_PWD]

except pymongo.errors.CollectionInvalid as collectionError:
    print(f"Error al conectar con la colección: {collectionError}")


"""
Se define una función la cual se encarga de generar un código de recuperación de contraseña
"""


def generate_code():
    code = []
    for i in range(CODE_LENGTH):
        code.append(random.choice(CODE_CHARS))
    return "".join(code)


"""
Se define una función la cual se encarga de enviar un correo con el código de recuperación de contraseña
"""


def send_code(email, user, code=generate_code()):
    body = f"""
        <div style="background-color: #e1f5fe71; font-size: 30px">
            <h1>
                <span style="color: #0f9ed5"
                    >Lamentamos que perdieras tu contraseña 😢</span
                >
            </h1>
            <h2>
                <span style="color: #9c27b0; font-size: 30px">
                    Pero no te preocupes, puedes recuperar tu cuenta escribiendo
                    el siguiente código de validación y siguiendo los pasos en
                    LAIA app 😄:
                </span>
            </h2>
            <code>
                <h1>
                    <span style="color: #e91e63; font-size: 70px">{code}</span>
                </h1>
            </code>
        </div>
    """
    subject = f"Recuper tu contraseña de LAIA app, {user} 😄"

    try:
        return resend.Emails.send(
            {
                "from": "laia-app@resend.dev",
                "to": email,
                "subject": subject,
                "html": body,
            }
        )
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return {"error": f"Error al enviar el correo: {e}"}


"""
Se define una función la cual se encarga de guardar el codigo de recuperación en la base de datos
Recibe un diccionario con usuario y correo
Retorna un mensaje de éxito o error
"""


def recovery_user_code(doc):
    try:
        code = generate_code()
        send_code(doc.get("email"), doc.get("user"), code)

        data = {"user": doc.get("user"), "code": code}
        save_recovery_code(data)
        return {"message": "Código de recuperación enviado"}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": f"Error interno del servidor:\n{e}"}


"""
Se define una función la cual se encarga de guardar el codigo de recuperación en la base de datos
Recibe un diccionario con usuario y correo
Retorna un mensaje de éxito o error
"""


def save_recovery_code(doc):
    try:
        collection.insert_one(doc)
        return True

    except Exception as e:
        print(f"Error: {e}")
        return {"error": f"Error interno del servidor:\n{e}"}


"""
Se define una función la cual se encarga de validar el codigo de recuperación en la base de datos
Recibe un diccionario con usuario y correo
Retorna un mensaje de éxito o error
"""


def validate_recovery_code(user, code):
    try:
        data = collection.find_one({"user": user})
        data["_id"] = str(data.get("_id"))

        return code == data.get("code")

    except Exception as e:
        print(f"Error: {e}")
        return {"error": f"Error interno del servidor:\n{e}"}


"""
Se define una función la cual se encarga de eliminar el codigo de recuperación en la base de datos
Recibe un diccionario con usuario y correo
Retorna un mensaje de éxito o error
"""


def delete_recovery_code(doc):
    try:
        collection.delete_one({"user": doc.get("user")})

        return True

    except Exception as e:
        print(f"Error: {e}")
        return {"error": f"Error interno del servidor:\n{e}"}
