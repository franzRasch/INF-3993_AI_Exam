from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
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



def smart_split_documents(documents: list[Document], is_exam: bool = False) -> list[Document]:
    """
    If the document is an exam, split by 'Task', else do standard recursive chunking.
    """
    if is_exam:
        task_docs = split_documents_by_task(documents)
        return split_documents(task_docs)
    else:
        return split_documents(documents)
    



