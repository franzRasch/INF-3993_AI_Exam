from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import TextLoader

import pymupdf
import os

# --- CONFIG ---
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"

def extract_text_from_pdf(file_path: str) -> str:
    with pymupdf.open(file_path) as pdf:
        return "".join(page.get_text() for page in pdf)

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    

def load_documents(folder_path: str) -> list[Document]:
    """Returns a list of documents from the specified folder."""
    documents = []

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        if not os.path.isfile(full_path):
            continue  # Skip directories

        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(full_path)
        elif filename.endswith(".txt"):
            text = extract_text_from_txt(full_path)
        else:
            continue  # Skip unsupported files

        documents.append(Document(page_content=text, metadata={"source": filename}))

    return documents






