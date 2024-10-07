import os
import warnings
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
warnings.filterwarnings("ignore", category=DeprecationWarning)
