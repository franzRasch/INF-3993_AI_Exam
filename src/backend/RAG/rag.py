from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

import pymupdf
import os

from local_loader import load_documents
from splitter import smart_split_documents

# --- CONFIG ---
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"



if __name__ == "__main__":
    # Step 1: get the path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 2: go one directory up
    base_dir = os.path.abspath(os.path.join(current_dir, ".."))

    # Step 3: build full path to the file in data/INF-3701
    file_path = os.path.join(base_dir, "data", "INF-3701")
    print(f"File path: {file_path}")
    # Step 4: call your function
    docs = load_documents(file_path)

    # Step 5: split the documents depended on the document
    chunks = smart_split_documents(docs, is_exam=True)
    for chunk in chunks:
        print(f"chunk: {chunk}")

