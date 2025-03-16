# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DB_PATH = "./chroma_db"