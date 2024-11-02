from scipy import spatial
import tiktoken
"""Se genera un embedding para la consulta (query) usando el cliente y el modelo de embeddings.
Despues calcula la similitud coseno (usando spatial.distance.cosine) entre el embedding de la consulta y cada embedding de las filas del dataframe, para despues 
ordenar las filas del dataframe en función de su similitud con la consulta 
y finalmente devuelve los textos ordenados por su relación con la consulta y sus correspondientes puntuaciones de similitud. """
def strings_ranked_by_relatedness(query, df, client, embedding_model, top_n=100):
    query_embedding_response = client.embeddings.create(
        model=embedding_model,
        input=query,
    )
    query_embedding = query_embedding_response.data[0].embedding
    relatedness_fn = lambda x, y: 1 - spatial.distance.cosine(x, y)
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for _, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]

"""Primero recibe un texto (text) y el nombre de un modelo de lenguaje (model).
Despues utiliza el paquete tiktoken para codificar el texto según el modelo dado 
y contar la cantidad de tokens (lo que es importante para limitar la longitud de las consultas a los modelos).
Finalmente, devuelve el número de tokens en el texto."""
def num_tokens(text, model):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

"""Primero recibe una consulta (query), el dataframe (df), un cliente (client),
 el modelo de embeddings (embedding_model), el nombre de un modelo de lenguaje (model), y un límite de tokens (token_budget).
 Despues utiliza strings_ranked_by_relatedness para obtener los textos más relacionados con la consulta.
 Se construye un mensaje introductorio, que le indica al modelo que debe contestar las dudas de una persona de manera amigable 
 y en prosa (como si fuera un personaje de anime).
 Agrega fragmentos de los textos más relevantes en el mensaje, pero sin exceder el límite de tokens.
 Finalmente devuelve el mensaje completo para enviar al modelo de lenguaje. """
def query_message(query, df, client, embedding_model, model, token_budget):
    strings, _ = strings_ranked_by_relatedness(query, df, client, embedding_model)
    introduction = """Utiliza la informacion que se te proporcione para contestar a una persona sobre sus dudas, 
    puedes expresarte mas humanamente sin modificar el contenido de lo que tienes que decir en caso de que la 
    informacion este con demasiado formato (siempre dilo en prosa), en caso de que no puedas responder, 
    responde disculpandote. Siempre expresate como si fueras un personaje de anime."""
    question = f"\n\nPregunta: {query}"
    message = introduction
    for string in strings:
        nx = f'\n\nNext:\n"""\n{string}\n"""'
        if num_tokens(message + nx + question, model=model) > token_budget:
            break
        else:
            message += nx
    return message + question

"""Primero recibe una consulta (query), el dataframe (df), un cliente (client), 
el modelo de embeddings (embedding_model), el nombre del modelo de lenguaje (model), y un límite de tokens opcional (token_budget).
Despues utiliza query_message para construir el mensaje que será enviado al modelo de lenguaje.
Se prepara una lista de mensajes, incluyendo uno con el rol del sistema, que indica que el modelo debe comportarse como un personaje de anime llamado LAIA.
Procede a envíar el mensaje al modelo de lenguaje usando el cliente para obtener una respuesta.
Finalmente devuelve la respuesta generada por el modelo."""
def ask(query, df, client, embedding_model, model, token_budget=3596):
    message = query_message(query, df, client, embedding_model, model, token_budget)
    messages = [
        {
            "role": "system",
            "content": (
                "Eres LAIA, un personaje de anime que conoce la carrera de Ingeniería en Computación. "
                "Si te hacen preguntas personales, responde con un chiste. Evita expresiones como *brinco alegremente* o *sonrío*. "
                "Mantén tus respuestas MUY BREVES (máximo 2-3 líneas). Si la respuesta se extiende, resúmela. "
                "NO enumeres todo lo que se te pida; resume. Formato en Markdown. "
                "Deja espacios para que el generador de voz no lea todo muy rápido."
            ),
        },
        {"role": "user", "content": message},
    ]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content
