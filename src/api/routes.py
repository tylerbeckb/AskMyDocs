from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from src.api.schemas import QueryRequest, QueryResponse, DocumentUpLoadRequest, ErrorResponse
from src.rag.generator import AnswerGenerator
from src.rag.indexing import DocumentIndexer
from src.utils.vector_store import VectorStore
from src.models.embeddings import EmbeddingsModel
from src.rag.retriever import Retriever
from src.models.llm import LLMService
import os
import uuid
from typing import Dict

router = APIRouter()

# Dependency to get RAG components
def get_rag_components():
    # Initialise embedding model
    embedding_model = EmbeddingsModel(model_type="openai")

    # Initialise vector store
    vector_store = VectorStore(embedding_model=embedding_model, db_type="faiss")

    # Load vector store if it exists
    persist_dir = "data/vector_store"
    if os.path.exists(persist_dir):
        vector_store.load(persist_dir)

    # Initialise retriever
    retriever = Retriever(vector_store=vector_store)

    # Initialise LLM service
    llm_service = LLMService(model_name="gpt-3.5-turbo", temparture=0.0)

    # Initialise answer generator
    answer_generator = AnswerGenerator(retriever=retriever, llm_service=llm_service)

    return {
        "indexer": DocumentIndexer(embedding_model_type="openai"),
        "answer_generator": answer_generator,
    }