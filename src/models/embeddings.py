from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.embeddings.base import Embeddings
from typing import List
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class DeepSeekEmbeddings(Embeddings):
    """Custom embeddings class for DeepSeek API"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DeepSeek API key is required")
        self.api_url = "https://api.deepseek.com/v1/embeddings"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for a list of documents"""
        results = []
        for text in texts:
            results.append(self.embed_query(text))
        return results
    
    def embed_query(self, text: str) -> List[float]:
        """Get embedding for a single query"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model": "deepseek-chat"
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise ValueError(f"Error from DeepSeek API: {response.text}")
        data = response.json()
        return data["data"][0]["embedding"]

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
