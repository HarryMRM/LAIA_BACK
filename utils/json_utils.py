from scipy import spatial
import tiktoken

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

def num_tokens(text, model):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

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

def ask(query, df, client, embedding_model, model, token_budget=3596):
    message = query_message(query, df, client, embedding_model, model, token_budget)
    messages = [
        {"role": "system", "content": "Eres un personaje de anime llamado LAIA que conoce la carrera de Ingenieria en Computacion, si la pregunta es personal puedes responder con un chiste."},
        {"role": "user", "content": message},
    ]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content
