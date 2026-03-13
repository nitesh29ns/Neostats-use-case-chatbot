import os
import io
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from uuid import uuid4
from models.embeddings import get_embedding_funcation
from utils.logger import lg
from config.config import UPLOADED_DOCUMENTS_EMBEDDINGS, UPLOADED_DOCUMNETS_DIR
import docx

lg.info("=============================================================== VECTOR DATABASE ===============================================================")


class vectordb:

    def __init__(self, file_paths: list, chroma_path: str = UPLOADED_DOCUMENTS_EMBEDDINGS):
        try:
            if isinstance(file_paths, str):
                file_paths = [file_paths]  # convert single file to list

            self.file_paths = file_paths
            self.chroma_path = chroma_path

            lg.info(f"VectorDB initialized | file_paths={file_paths} | chroma_path={chroma_path}")

        except Exception as e:
            lg.error(f"Initialization failed: {str(e)}")
            raise e

    def load_documents_from_uploaded(self):
        try:
            os.makedirs(UPLOADED_DOCUMNETS_DIR, exist_ok=True)
            all_documents = []

            
            if not isinstance(self.file_paths, list):
                self.file_paths = [self.file_paths]

            saved_file_paths = []

            
            for uploaded_file in self.file_paths:
                file_path = os.path.join(UPLOADED_DOCUMNETS_DIR, uploaded_file.name)
                
               
                if uploaded_file.name.lower().endswith(".txt"):
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(uploaded_file.getvalue().decode("utf-8"))
                else:
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())  

                saved_file_paths.append(file_path)

            
            for file_path in saved_file_paths:
                lg.info(f"Loading document: {file_path}")
                ext = os.path.splitext(file_path)[1].lower()

                if ext == ".pdf":
                    lg.info("Detected PDF file")
                    loader = PyPDFLoader(file_path)
                elif ext == ".txt":
                    lg.info("Detected TXT file")
                    loader = TextLoader(file_path)
                elif ext == ".docx":
                    lg.info("Detected DOCX file")
                    loader = Docx2txtLoader(file_path)
                else:
                    lg.error(f"Unsupported file format: {file_path}")
                    raise ValueError(f"Unsupported file format: {file_path}. Use PDF, TXT, or DOCX.")

                documents = loader.load()
                lg.info(f"Document loaded successfully | pages={len(documents)}")
                all_documents.extend(documents)

            lg.info(f"Total documents loaded from all files: {len(all_documents)}")
            return all_documents

        except Exception as e:
            lg.error(f"Document loading failed: {str(e)}")
            raise e
    

    def split_documents(self, documents: list):
        try:
            lg.info("Starting document chunking")

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ". ", " "]
            )

            chunks = text_splitter.split_documents(documents)

            lg.info(f"Chunking completed | total_chunks={len(chunks)}")

            return chunks

        except Exception as e:
            lg.error(f"Chunking failed: {str(e)}")
            raise e

    def add_to_chroma(self, chunks: list):
        try:
            lg.info("Initializing Chroma vector database")

            db = Chroma(
                persist_directory=self.chroma_path,
                embedding_function=get_embedding_funcation()
            )

            if len(chunks):
                lg.info(f"Adding chunks to vector DB | chunks={len(chunks)}")
                chunks_ids = [str(uuid4()) for _ in range(len(chunks))]
                db.add_documents(chunks, ids=chunks_ids)
                lg.info("Documents successfully added to vector database")
                return "vector db is created."
            else:
                lg.warning("No chunks found to insert into vector DB")

        except Exception as e:
            lg.error(f"Vector DB insertion failed: {str(e)}")
            raise e

    def upload_to_vectordb(self):
        try:
            lg.info("Starting vector DB pipeline")
            documents = self.load_documents_from_uploaded()
            chunks = self.split_documents(documents)
            self.add_to_chroma(chunks)
            lg.info("Vector DB pipeline completed successfully")
            return "db created."

        except Exception as e:
            lg.error(f"Vector DB pipeline failed: {str(e)}")
            raise e
        


# class vectordb:

#     def __init__(self, file_path: str, chroma_path: str):
#         try:
#             self.file_path = file_path
#             self.chroma_path = chroma_path

#             lg.info(f"VectorDB initialized | file_path={file_path} | chroma_path={chroma_path}")

#         except Exception as e:
#             lg.error(f"Initialization failed: {str(e)}")
#             raise e


#     def load_documents(self):
#         try:
#             lg.info(f"Loading document: {self.file_path}")

#             ext = os.path.splitext(self.file_path)[1].lower()

#             if ext == ".pdf":
#                 lg.info("Detected PDF file")
#                 loader = PyPDFLoader(self.file_path)

#             elif ext == ".txt":
#                 lg.info("Detected TXT file")
#                 loader = TextLoader(self.file_path)

#             elif ext == ".docx":
#                 lg.info("Detected DOCX file")
#                 loader = Docx2txtLoader(self.file_path)

#             else:
#                 lg.error("Unsupported file format")
#                 raise ValueError("Unsupported file format. Use PDF, TXT, or DOCX.")

#             documents = loader.load()

#             lg.info(f"Document loaded successfully | pages={len(documents)}")

#             return documents

#         except Exception as e:
#             lg.error(f"Document loading failed: {str(e)}")
#             raise e


#     def split_documents(self, documents: list):
#         try:
#             lg.info("Starting document chunking")

#             # text_splitter = RecursiveCharacterTextSplitter(
#             #     chunk_size=800,
#             #     chunk_overlap=80,
#             #     length_function=len,
#             #     is_separator_regex=False,
#             # )
#             text_splitter = RecursiveCharacterTextSplitter(
#                             chunk_size=500,
#                             chunk_overlap=50,
#                             separators=["\n\n", "\n", ". ", " "]
#                             )

#             chunks = text_splitter.split_documents(documents)

#             lg.info(f"Chunking completed | total_chunks={len(chunks)}")

#             return chunks

#         except Exception as e:
#             lg.error(f"Chunking failed: {str(e)}")
#             raise e


#     def add_to_chroma(self, chunks: list):
#         try:
#             lg.info("Initializing Chroma vector database")

#             db = Chroma(
#                 persist_directory=self.chroma_path,
#                 embedding_function=get_embedding_funcation()
#             )

#             if len(chunks):

#                 lg.info(f"Adding chunks to vector DB | chunks={len(chunks)}")

#                 chunks_ids = [str(uuid4()) for _ in range(len(chunks))]

#                 db.add_documents(chunks, ids=chunks_ids)

#                 lg.info("Documents successfully added to vector database")

#                 return "vector db is created."

#             else:
#                 lg.warning("No chunks found to insert into vector DB")

#         except Exception as e:
#             lg.error(f"Vector DB insertion failed: {str(e)}")
#             raise e


#     def upload_to_vectordb(self):
#         try:
#             lg.info("Starting vector DB pipeline")

#             documents = self.load_documents()

#             chunks = self.split_documents(documents)

#             self.add_to_chroma(chunks)

#             lg.info("Vector DB pipeline completed successfully")

#             return "db created."

#         except Exception as e:
#             lg.error(f"Vector DB pipeline failed: {str(e)}")
#             raise e