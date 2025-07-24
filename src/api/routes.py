from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from src.api.schemas import QueryRequest, QueryResponse, DocumentUploadResponse, ErrorResponse
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
    embedding_model = EmbeddingsModel(model_type="deepseek")

    # Initialise vector store
    vector_store = VectorStore(embedding_model=embedding_model, db_type="faiss")

    # Load vector store if it exists
    persist_dir = "data/vector_store"
    if os.path.exists(persist_dir):
        vector_store.load(persist_dir)

    # Initialise retriever
    retriever = Retriever(vector_store=vector_store)

    # Initialise LLM service
    llm_service = LLMService(model_name="deepseek-chat", temparture=0.0)

    # Initialise answer generator
    answer_generator = AnswerGenerator(retriever=retriever, llm_service=llm_service)

    return {
        "indexer": DocumentIndexer(embedding_model_type="deepseek"),
        "answer_generator": answer_generator,
    }

@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest, components = Depends(get_rag_components)):
    """Query the document knowledge base"""
    answer_generator = components["answer_generator"]

    try:
        result = answer_generator.generate_answer(
            query=request.query,
            top_k=request.top_k
        )
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document (
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    components = Depends(get_rag_components)
):
    """Upload and index a document."""
    indexer = components["indexer"]

    # Save uploaded file
    file_path = f"data/pdfs/{uuid.uuid4()}_{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Index the document in the background
    def index_document():
        try:
            indexer.index_pdf(pdf_path=file_path, persist_dir="data/vector_store")
        except Exception as e:
            print(f"Error indexing document: {e}")

    # Add indexing task to background
    background_tasks.add_task(index_document)

    return DocumentUploadResponse(
        filename=file.filename,
        chunks=0, # Place holder
        status="processing"
    )