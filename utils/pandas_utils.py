"""Se importa pandas, librería para trabajar con datos tipo tablas (dataframes),
 y ast, que ayuda a convertir texto en objetos de Python. En este caso, se usa para 
 transformar las listas que están guardadas como texto en listas de verdad."""
import pandas as pd
import ast

"""La función load_embeddings(embeddings_path: str) -> pd.DataFrame: recibe la ruta de un archivo CSV 
(donde se guardan los embeddings) y devuelve un dataframe de pandas.
Despues se lee el archivo CSV y lo convierte en un dataframe.
Posteriormente se toma valor de la columna 'embedding' (que son listas, pero están guardadas como texto)
y las convierte en listas reales usando ast.literal_eval(). 
Finalmente, devuelve el dataframe ya cargado, con las listas de embeddings listas para ser usadas.
"""
def load_embeddings(embeddings_path: str) -> pd.DataFrame:
    df = pd.read_csv(embeddings_path)
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    return df