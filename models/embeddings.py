from langchain_nomic import NomicEmbeddings  
from config.config import NORMIC_EMBEDDING, EMBEDDING_MODEL_NAME


def get_embedding_funcation():
        embedding = NomicEmbeddings(
            model=EMBEDDING_MODEL_NAME,)
        return embedding
