import chromadb
import os
from .local_loader import load_documents
from .splitter import smart_split_documents
import torch


class KnowledgeBase:
    def __init__(self, collection_name: str):
        self.client = chromadb.Client()
        self.collection = self.get_collection(collection_name)
        torch.device("cpu")
        self.ef = (
            chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )

    def get_collection(self, collection_name: str):
        collection = self.client.get_or_create_collection(name=collection_name)
        return collection

    def store_in_collection(self, chunks):
        docs = list()
        ids = list()
        metadata = list()
        for i, chunk in enumerate(chunks):
            docs.append(chunk)
            ids.append("id" + str(i))
            metadata.append(chunk.metadata)
            self.collection.add(
                documents=[chunk.page_content],
                metadata=[chunk.metadata],
                ids=["id" + str(i)],
            )

    def build_collection(self, path: str):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.abspath(os.path.join(current_dir, ".."))
        file_path = os.path.join(base_dir, "data", path)
        docs = load_documents(file_path)
        new_documents = list()
        for doc in docs:
            filename = doc.metadata["source"]
            doc_items = self.collection.get(where={"metadata": filename})
            if len(doc_items["ids"]) == 0:
                new_documents.append(doc)
        chunks = smart_split_documents(new_documents, is_exam=False)
        self.store_in_collection(chunks)

    def search_collection(self, search: str):
        words = search.split()
        embeddings = self.ef(words)
        result = self.collection.query(query_embeddings=embeddings, n_results=2)
        return result
