import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

NORMIC_EMBEDDING = os.getenv("NORMIC_EMBEDDING")

WEB_SEARCH_API = os.getenv("WEB_SEARCH_API")

MODEL_NAME = "llama-3.3-70b-versatile"

EMBEDDING_MODEL_NAME = "nomic-embed-text-v1.5"

UPLOADED_DOCUMENTS_EMBEDDINGS = os.path.abspath("./uploaded_data_embeddings") 

UPLOADED_DOCUMNETS_DIR =  os.path.abspath("./uploaded_documents")

MAX_RESEARCH_SUGGESTIONS = 3