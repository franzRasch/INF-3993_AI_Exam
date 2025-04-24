from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import TextLoader

import pymupdf
import os

# --- CONFIG ---
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR = "./chroma_db"




def split_documents_by_task(documents: list[Document]) -> list[Document]:
    task_docs = []
    for doc in documents:
        parts = doc.page_content.split("Task ")
        for part in parts:
            clean = part.strip()
            if clean:
                content = "Task " + clean  # add "Task" back
                task_docs.append(Document(page_content=content, metadata=doc.metadata))
    return task_docs




def split_documents(documents: list[Document], chunk_size=1000, overlap=200) -> list[Document]:
    """
    Split LangChain Document objects into smaller chunks for embedding and retrieval.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)  # ✅ Correct method

# --- STEP 2: Embed and Store into Chroma ---

def embed_documents() -> HuggingFaceBgeEmbeddings:
    return HuggingFaceBgeEmbeddings(model_name=MODEL_NAME)

def extract_text_from_pdf(file_path: str) -> str:
    with pymupdf.open(file_path) as pdf:
        return "".join(page.get_text() for page in pdf)

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_documents(folder_path: str) -> list[Document]:
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



def smart_split_documents(documents: list[Document], is_exam: bool = False) -> list[Document]:
    """
    If the document is an exam, split by 'Task', else do standard recursive chunking.
    """
    if is_exam:
        task_docs = split_documents_by_task(documents)
        return split_documents(task_docs)
    else:
        return split_documents(documents)
    



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

