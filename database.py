# database.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma  # Updated import
import streamlit as st
from config import EMBEDDING_MODEL_NAME, CHROMA_DB_PATH

def initialize_vector_db():
    """Initialize and return the Chroma vector database."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    try:
        vector_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        return vector_db
    except Exception as e:
        st.error(f"Error loading Chroma DB: {e}")
        st.stop()