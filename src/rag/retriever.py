from src.utils.vector_store import VectorStore
from typing import Dict, Any, Optional, List
from langchain.schema import Document

class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        """Retrieve documents based on a query"""
        if not self.vector_store:
            raise ValueError("Vector store is not initialized.")
        
        results = self.vector_store.similarity_search(query, k=top_k)
        return results