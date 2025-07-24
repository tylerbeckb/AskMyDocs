from src.utils.vector_store import VectorStore
from typing import List
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
    
    def format_context(self, documents: List[Document]) -> str:
        """Format retrieved documents into a context string"""
        context_parts = []

        for i, doc in enumerate(documents):
            # Format each document with its metadata
            source = doc.metadata.get("source", "Unknown")
            section = doc.metadata.get("section", "General")

            context_part = f"[Documment {i+1}] From: {source}, Section: {section}\n{doc.page_content}\n"
            context_parts.append(context_part)

        return "\n".join(context_parts)