# vectorstore.py
from langchain_chroma import Chroma
import shutil
import os
from .embedder import get_embedder


def store_documents(docs, path="chroma_db"):
    # Delete the existing database folder
    if os.path.exists(path):
        shutil.rmtree(path)

    # Create a new database from the documents
    embedder = get_embedder()
    Chroma.from_documents(documents=docs, embedding=embedder, persist_directory=path)

def store_documents_append(docs, path="chroma_db"):
    embedder = get_embedder()
    try:
        db = Chroma(persist_directory=path, embedding_function=embedder)
        db.add_documents(docs)
    except:
        # If the DB doesn't exist yet, create it
        db = Chroma.from_documents(documents=docs, embedding=embedder, persist_directory=path)
    db.persist()


def load_vectorstore(path="chroma_db"):
    return Chroma(persist_directory=path, embedding_function=get_embedder())


