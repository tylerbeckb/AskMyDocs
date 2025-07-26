from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.exceptions import DocumentProcessingError, VectorStoreError, LLMError, DocumentNotFoundError
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AskMyDocs API",
    description="A RAG-based AI Assistant for Travel Insurance PDFs",
    version="1.0.0",
)

# Add exception handlers
@app.exception_handler(DocumentProcessingError)
async def document_processing_error_handler(request: Request, exc: DocumentProcessingError):
    logging.error(f"Document Processing Error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error processing the document.", "details": str(exc)}
    )

@app.exception_handler(VectorStoreError)
async def vector_store_exception_handler(request: Request, exc: VectorStoreError):
    logging.error(f"Vector store error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Vector database operation failed", "details": str(exc)}
    )

@app.exception_handler(LLMError)
async def llm_exception_handler(request: Request, exc: LLMError):
    logging.error(f"LLM error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"error": "Language model service unavailable", "details": str(exc)}
    )

@app.exception_handler(DocumentNotFoundError)
async def document_not_found_exception_handler(request: Request, exc: DocumentNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Document not found", "details": str(exc)}
    )

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix="/api")

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to AskMyDocs API. Go to /docs for documentation."}

# Run the applicaiton wiht uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)