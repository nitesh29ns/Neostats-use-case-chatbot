from langchain_chroma import Chroma
from models.embeddings import get_embedding_funcation
from utils.logger import lg
from config.config import UPLOADED_DOCUMENTS_EMBEDDINGS

lg.info("=============================================================== RAG- RETRIEVER ===============================================================")


def rag_content(output_type:str,query:str,chroma_path=UPLOADED_DOCUMENTS_EMBEDDINGS)-> list:
    """ retrieval from vector db based on the user query"""
    try:
        lg.info("Initializing retrieval from vector db")

        if output_type == "Concise":
            k = 5
        else:
            k = 10
        db = Chroma(
            persist_directory=chroma_path,
            embedding_function=get_embedding_funcation()
        )

        retriever = db.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k":k,
                "fetch_k":20
            }
        )

        results = retriever.invoke(query)

        results = [doc.page_content for doc in results]

        lg.info("Data from vectordb Retrieved successfully")
        
        return results
    
    except Exception as e:
        lg.error(f"Data from vectordb Retrieved failed: {str(e)}")
        raise e