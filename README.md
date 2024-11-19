# Backend para el sistema LAIA.

Backend para el sistema LAIA.

## Requerimientos

-   Python 3.12.5
-   pip 24.2

## Instalación

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/laia-backend.git
    cd laia-backend
    ```
2. Crear y activar un entorno virtual:

    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3. Instalar las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Crea una carpeta audio en la raiz.

5. Crea una carpeta data en la raizy agrega tu archivo .csv de embeddings en la carpeta

6. Cambia el archivo openai_client.py segun el nombre del archivo.

7. Crear un archivo .env y agregar lo siguiente:
    ```bash
    OPENAI_API_KEY="key"
    NARAKEET_API_KEY="key"

    MONGO_URI = "mongo_uri"
    MONGO_DATABASE_MSG = "mongo_messages_database_name"
    MONGO_COLLECTION_MSG = "mongo_messages_collection_name"
    MONGO_DATABASE_USR = "mongo_users_database_name"
    MONGO_COLLECTION_USR = "mongo_users_collection_name"
    MONGO_COLLECTION_TKN = "mongo_tokens_collection_name"
    
    RESEND_API_KEY = 'resend_api_key'

    CRYPTING_KEY = crypting key in python bytes
    TKN_EXP = expiration minutes for tokens in int
    ACCESS_SECRET = "access_token_secret"
    REFRESH_SECRET = "refresh_token_secret"
    ```

## Cómo ejecutar

1. Activar el entorno virtual:

    ```bash
    .\.venv\Scripts\activate
    ```

2. Ejecutar la aplicación Flask:
    ```bash
    flask run
    ```

## Diagrama de arquitectura y documentación

https://docs.google.com/document/d/1fsHj1lpDwu_kNGZiXYktd8fZ1TuaJ0GAI0N5jz-fsEE/edit?usp=sharing
