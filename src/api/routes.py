from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks, status
from src.api.schemas import QueryRequest, QueryResponse, DocumentUploadResponse, ErrorResponse
from src.api.exceptions import DocumentProcessingError, VectorStoreError, LLMError, DocumentNotFoundError
from src.rag.generator import AnswerGenerator
from src.rag.indexing import DocumentIndexer
from src.utils.vector_store import VectorStore
from src.models.embeddings import EmbeddingModel
from src.rag.retriever import Retriever
from src.models.llm import LLMService
import os
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency to get RAG components
def get_rag_components():
    try:
        # Initialise embedding model
        embedding_model = EmbeddingModel(model_type="deepseek")

        # Initialise vector store
        vector_store = VectorStore(embedding_model=embedding_model, db_type="faiss")

        # Load vector store if it exists
        persist_dir = "data/vector_store"
        if os.path.exists(persist_dir):
            vector_store.load(persist_dir)

        # Initialise retriever
        retriever = Retriever(vector_store=vector_store)

        # Initialise LLM service
        llm_service = LLMService(model_name="deepseek-chat", temperarture=0.0)

        # Initialise answer generator
        answer_generator = AnswerGenerator(retriever=retriever, llm_service=llm_service)

        return {
            "indexer": DocumentIndexer(embedding_model_type="deepseek"),
            "answer_generator": answer_generator,
        }
    except Exception as e:
        logger.error(f"Failed to initialize RAG components: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize application components"
        )

@router.post("/query", response_model=QueryResponse, responses={
    400: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
    503: {"model": ErrorResponse}
})
async def query_documents(request: QueryRequest, components = Depends(get_rag_components)):
    """Query the document knowledge base"""
    answer_generator = components["answer_generator"]

    if not request.query or len(request.query.strip()) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )

    try:
        #Check if vector store is empty
        if not answer_generator.retriever.vector_store.store:
            return QueryResponse(
                answer="No documents have been indexed yet. Please upload a document first.",
                sources=[]
            )
        result = answer_generator.generate_answer(
            query=request.query,
            top_k=request.top_k
        )
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except LLMError as e:
        logger.error(f"LLM error during query: {e}")
        raise
    except VectorStoreError as e:
        logger.error(f"Vector store error during query: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating answer: {str(e)}"
        )

@router.post("/upload", response_model=DocumentUploadResponse, responses={
    400: {"model": ErrorResponse},
    415: {"model": ErrorResponse},
    500: {"model": ErrorResponse}
})
async def upload_document (
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    components = Depends(get_rag_components)
):
    """Upload and index a document."""
    indexer = components["indexer"]

    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are supported"
        )

    try:
        # Create directory if it doesn't exist
        os.makedirs("data/pdfs", exist_ok=True)

        # Save uploaded file
        file_path = f"data/pdfs/{uuid.uuid4()}_{file.filename}"

        with open(file_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Uploaded file is empty"
                )
            f.write(content)

        # Index the document in the background
        def index_document():
            try:
                result = indexer.index_pdf(
                    pdf_path=file_path,
                    persist_directory="data/vector_store"
                )
                logger.info(f"Successfully indexed document: {file.filename}")
                return result
            except Exception as e:
                logger.error(f"Error indexing document {file.filename}: {str(e)}")
                # Delete the file if indexing failed
                try:
                    os.remove(file_path)
                except:
                    pass
                raise DocumentProcessingError(f"Failed to process document: {str(e)}")

        # Add indexing task to background
        background_tasks.add_task(index_document)

        return DocumentUploadResponse(
            filename=file.filename,
            chunks=0, # Place holder
            status="processing"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )