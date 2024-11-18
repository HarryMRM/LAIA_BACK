import ollama
import openai
from config import OPENAI_API_KEY
from utils.json_utils import ask_ollama
from utils.pandas_utils import load_embeddings
openai.api_key = OPENAI_API_KEY
embeddings_path = "data/uabcEmb.csv"

def generate_response(input_text):
    client = ollama
    clientEmb = openai.OpenAI()
    df = load_embeddings(embeddings_path)
    answer = ask_ollama(input_text, df, client, clientEmb, "text-embedding-ada-002", "llama3.2")
    return answer