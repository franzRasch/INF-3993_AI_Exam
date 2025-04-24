from langchain_community.vectorstores import Chroma
from embedder import get_embedder

def store_documents(docs, path="chroma_db"):
    embedder = get_embedder()
    db = Chroma.from_documents(documents=docs, embedding=embedder, persist_directory=path)
    db.persist()

def load_vectorstore(path="chroma_db"):
    return Chroma(persist_directory=path, embedding_function=get_embedder())

def query_vectorstore(query: str, k=3, path="chroma_db"):
    db = load_vectorstore(path)
    results = db.similarity_search(query, k=k)
    return [doc.page_content for doc in results]
