import os
import sys
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))



def get_chatgroq_model():
    """Initialize and return the Groq chat model"""
    try:
        # Initialize the Groq chat model with the API key
        groq_model = ChatGroq(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
        )
        return groq_model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")