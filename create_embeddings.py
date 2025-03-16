import os
from dotenv import load_dotenv
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables
load_dotenv()

# Initialize HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("HuggingFace embeddings initialized successfully.")

# Load the test bank
test_bank = pd.read_csv("test.csv")
print("Test bank loaded successfully.")
print(f"Test bank columns: {test_bank.columns}")

# Function to chunk multiple rows together
def chunk_rows(rows, chunk_size=3):
    chunks = []
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i:i + chunk_size]
        chunk_text = "\n".join([
            f"Test Case {row['Sl No.']}:\n"
            f"Description: {row['Test Case Description']}\n"
            f"Steps: {row['Execution Steps']}\n"
            f"Expected Result: {row['Expected Result']}\n"
            for _, row in chunk.iterrows()
        ])
        chunks.append(chunk_text)
        print(f"Created chunk for rows {i+1} to {min(i+chunk_size, len(rows))}")
    return chunks

# Convert the test bank into chunks
chunk_size = 3  # Number of rows per chunk
documents = chunk_rows(test_bank, chunk_size)
print(f"Number of chunks created: {len(documents)}")
print(f"Sample chunk:\n{documents[0]}")  # Print the first chunk for verification

# Create Chroma DB
try:
    print("Creating Chroma DB...")
    vector_db = Chroma.from_texts(documents, embeddings, persist_directory="./chroma_db")
    print("Chroma DB created successfully.")
    print(f"Number of embeddings stored: {len(vector_db.get()['ids'])}")  # Print the number of embeddings stored
except Exception as e:
    print(f"Error creating Chroma DB: {e}")
    