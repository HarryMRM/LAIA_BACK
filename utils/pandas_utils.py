import pandas as pd
import ast

def load_embeddings(embeddings_path: str) -> pd.DataFrame:
    df = pd.read_csv(embeddings_path)
    df['embedding'] = df['embedding'].apply(ast.literal_eval)
    return df