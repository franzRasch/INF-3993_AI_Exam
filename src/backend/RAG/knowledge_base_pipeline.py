import os

from local_loader import load_documents
from splitter import smart_split_documents
from vectorstore import store_documents, store_documents
from Flashcards_llm_ollama import FlashCards

# --- CONFIG ---
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"

def insert_documents():
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

    # Store chunks in the vector store
    store_documents(chunks)
    print(f"Stored {len(chunks)} chunks into the vector store from {len(docs)} different PDFs.")
    return len(chunks)


def rag_pipeline(number_of_questions):    
    k_similarity = 3
    #k_similarity = insert_documents()
    trainer = FlashCards(
        topic="advanced distributed databases", 
        model_name="llama3.2:latest",
        k=k_similarity, 
        number_of_questions=number_of_questions
    )
    trainer.run()
