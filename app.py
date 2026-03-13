import streamlit as st
from streamlit_pdf_reader import pdf_reader
from docx import Document
import os
import sys
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.llm import get_chatgroq_model
from utils.retriever import rag_content
from utils.vector_db import vectordb
from langchain_core.prompts import ChatPromptTemplate
from config.config import UPLOADED_DOCUMNETS_DIR
from utils.prompts import SYSTEM_PROMPT
from utils.preprocessing_query import filtering_stop_words
from utils.web_search import web_search
from utils.research_paper_suggestions import top_3_suggestion


def get_chat_response(chat_model, messages, system_prompt,rag_data=None, output_type="Concise"):
    """Get response from the chat model"""
    try:
        # If RAG data exists, append it to the system prompt
        if rag_data and isinstance(rag_data, list) and len(rag_data) > 0:
            context_text = "\n".join(rag_data)
            system_prompt_with_rag = (
                f"{system_prompt}\n\n"
                f"Use the following documents to answer the user's question:\n{context_text}"
            )
        else:
            system_prompt_with_rag = system_prompt
        
         # Add output type instruction
        if output_type == "Concise":
            system_prompt_with_rag += "\n\nProvide short, summarized replies."
        elif output_type == "Detailed":
            system_prompt_with_rag += "\n\nProvide expanded, in-depth responses."

        # Prepare messages for the model
        formatted_messages = [SystemMessage(content=system_prompt_with_rag)]
        
        # Add conversation history
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
       
        # Get response from model
        response = chat_model.invoke(formatted_messages)
        return response.content
    
    except Exception as e:
        return f"Error getting response: {str(e)}"
    

def get_rag_context(output_type:str,query:str)->list:
    """Get context from vector db consists from user uploaded documents"""

    try:

        rag_retriever = rag_content(output_type=output_type,query=query)

        return rag_retriever
    except Exception as e :
        raise e


def instructions_page():
    """Instructions and setup page"""
    st.title("The Chatbot Blueprint")
    st.markdown("Welcome! Follow these instructions to set up and use the chatbot.")
    
    st.markdown("""
    ## 🔧 Installation
                
    
    First, install the required dependencies: (Add Additional Libraries base don your needs)
    
    ```bash
    pip install -r requirements.txt
    ```
    
    ## API Key Setup
    
    You'll need API keys from your chosen provider. Get them from:
    
    ### OpenAI
    - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
    - Create a new API key
    - Set the variables in config
    
    ### Groq
    - Visit [Groq Console](https://console.groq.com/keys)
    - Create a new API key
    - Set the variables in config
    
    ### Google Gemini
    - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
    - Create a new API key
    - Set the variables in config
    
    ## 📝 Available Models
    
    ### OpenAI Models
    Check [OpenAI Models Documentation](https://platform.openai.com/docs/models) for the latest available models.
    Popular models include:
    - `gpt-4o` - Latest GPT-4 Omni model
    - `gpt-4o-mini` - Faster, cost-effective version
    - `gpt-3.5-turbo` - Fast and affordable
    
    ### Groq Models
    Check [Groq Models Documentation](https://console.groq.com/docs/models) for available models.
    Popular models include:
    - `llama-3.1-70b-versatile` - Large, powerful model
    - `llama-3.1-8b-instant` - Fast, smaller model
    - `mixtral-8x7b-32768` - Good balance of speed and capability
    
    ### Google Gemini Models
    Check [Gemini Models Documentation](https://ai.google.dev/gemini-api/docs/models/gemini) for available models.
    Popular models include:
    - `gemini-1.5-pro` - Most capable model
    - `gemini-1.5-flash` - Fast and efficient
    - `gemini-pro` - Standard model
    
    ## How to Use
    
    1. **Go to the Chat page** (use the navigation in the sidebar)
    2. **Start chatting** once everything is configured!
    
    ## Tips
    
    - **System Prompts**: Customize the AI's personality and behavior
    - **Model Selection**: Different models have different capabilities and costs
    - **API Keys**: Can be entered in the app or set as environment variables
    - **Chat History**: Persists during your session but resets when you refresh
    
    ## Troubleshooting
    
    - **API Key Issues**: Make sure your API key is valid and has sufficient credits
    - **Model Not Found**: Check the provider's documentation for correct model names
    - **Connection Errors**: Verify your internet connection and API service status
    
    ---
    
    Ready to start chatting? Navigate to the **Chat** page using the sidebar! 
    """)


@st.dialog("Document Preview", width="large")
def preview_document(file):

    file_type = file.name.split(".")[-1].lower()

    # PDF Preview
    if file_type == "pdf":
        pdf_reader(file)

    # TXT Preview
    elif file_type == "txt":
        text = file.read().decode("utf-8")
        st.text_area("File Content", text, height=600)

    # DOCX Preview
    elif file_type in ["docx", "doc"]:
        doc = Document(file)
        text = "\n".join([p.text for p in doc.paragraphs])
        st.text_area("File Content", text, height=600)

    else:
        st.error("Unsupported file format")


def chat_page():
    """Main chat interface page"""

    st.title("🤖 SmartMentor - for `AI`, `ML`, `Physics`, `Math`, `CS` & `Economics`") 
    st.header("*Answering your questions with insights from AI, ML, Physics, Mathematics, CS, Statistics, and Economics. I also curate a list of seminal research papers relevant to our conversation.*")


    # type of output 
    output_type_button  = st.radio(
            "OUTPUT_TYPE:",
            ["Concise", "Detailed"],
            index=0)
    
    output_type = output_type_button


    # Determine which provider to use based on available API keys
    chat_model = get_chatgroq_model()
    

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    # if chat_model:
    if prompt := st.chat_input("Type your message here..."):
            
        # filter stop words
        query = filtering_stop_words(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display bot response
        with st.chat_message("assistant"):

            uploaded_docs = st.session_state.get("uploaded_docs", [])

            # which approach to be used.
            if len(uploaded_docs) > 0:
                st.info(f"{len(uploaded_docs)} document(s) available for RAG retrieval.")
                with st.spinner("Getting RAG from vectordb..."):

                    # Getting data from the vectordb
                    data = get_rag_context(output_type=output_type,query=query)

            else: 
                with st.spinner("Searching Web..."):
                    data = web_search(query=query,output_type=output_type)
        
            with st.spinner("Getting response..."):
                response = get_chat_response(chat_model, st.session_state.messages, SYSTEM_PROMPT,rag_data=data,output_type=output_type)
                st.markdown(response)

            with st.spinner("Relevent Research Papers..."):
                suggestions = top_3_suggestion(query=query)
                st.markdown("### 📚 Suggested Papers: From arix")

                for inx, paper in enumerate(suggestions,start=1):

                    authors = ", ".join(paper['authors'])
                    st.markdown(
                        f"Paper {inx}: "
                        f"**[{paper['title']}]({paper['url']})**  \n"
                        f"*Authors:* {authors}  \n"
                    )
                    st.markdown("---")  # horizontal separator
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
 

def sidebar_upload_section():

    st.subheader("➕ Upload Documents")

    # Upload multiple files
    uploaded_files = st.file_uploader(
        "Drag and drop files here",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    # Initialize session state for uploaded docs
    if "uploaded_docs" not in st.session_state:
        st.session_state["uploaded_docs"] = []

    # Add new files to session state
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [f.name for f in st.session_state["uploaded_docs"]]:
                st.session_state["uploaded_docs"].append(file)
                st.success(f"{file.name} uploaded successfully")

    # Process uploaded files into vector DB 
    if st.session_state["uploaded_docs"]:
        files = [file for file in st.session_state["uploaded_docs"]]

        with st.spinner("Processing documents into vector DB..."):
            db = vectordb(file_paths=files)
            res = db.upload_to_vectordb()
            st.success(f"{res} Done! ✅")

        # Display uploaded documents with preview buttons
        st.markdown("### Uploaded Documents")
        for file in st.session_state["uploaded_docs"]:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(file.name)
            with col2:
                if st.button("📄 View", key=file.name):
                    preview_document(file)

    # Return the list of uploaded files
    return st.session_state["uploaded_docs"]


def main():
    st.set_page_config(
        page_title="LangChain Multi-Provider ChatBot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Navigation
    with st.sidebar:
        st.title("Navigation")
        page = st.radio(
            "Go to:",
            ["Chat", "Instructions"],
            index=0
        )

        # Call upload sidebar function
        uploaded_docs = sidebar_upload_section()

        # Add clear chat button in sidebar for chat page
        if page == "Chat":
            st.divider()
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    

    # Route to appropriate page
    if page == "Instructions":
        instructions_page()
    
    if page == "Chat":
        chat_page()

if __name__ == "__main__":
    main()