from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from typing import List
import os

class EmbeddingModel:
    def __init__(self, model_type="openai"):
        self.model_type = model_type
        
        if model_type == "openai":
            self.model = OpenAIEmbeddings()
        elif model_type == "huggingface":
            self.model_type = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")
        else:
            raise ValueError("Unsupported model type. Choose 'openai' or 'huggingface'.")
        
    def embed_text(self, text: str) -> List[float]:
        """Convert a single text into an embedding vector"""
        return self.model.embed_query(text)
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Convert a list of documents into embedding vectors"""
        return self.model.embed_documents(documents)
