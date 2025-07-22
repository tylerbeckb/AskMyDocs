from langchain.vectorstores import FAISS
from langchain.schema import Document
from src.models.embeddings import EmbeddingModel
from typing import List, Dict, Any, Optional
import os

class VectorStore:
    def __init__(self, embedding_model: EmbeddingModel, db_type="faiss"):
        self.embedding_model = embedding_model.model
        self.db_type = db_type
        self.store = None

    def create_from_documents(self, documents: List[Document], persist_directory: Optional[str] = None):
        """Create a vector store from documents"""
        if self.db_type == "faiss":
            self.store = FAISS.from_documents(documents, self.embedding_model)
            
            # Save if directory is provided
            if persist_directory:
                os.makedirs(persist_directory, exist_ok=True)
                self.store.save_local(persist_directory)
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
        
        return self.store