from src.data.loader import DocumentLoader
from src.data.processor import DocumentProcessor
from src.utils.vector_store import VectorStore
from src.models.embeddings import EmbeddingModel
from src.utils.pdf_parser import PDFParser
from typing import Dict, Any, Optional
import os

class DocumentIndexer:
    def __init__(self, embedding_model_type = "openai", vector_store_type = "faiss", chunk_strategy = "insurance"):
        self.loader = DocumentLoader()
        self.processor = DocumentProcessor()
        self.embedding_model = EmbeddingModel(model_type=embedding_model_type)
        self.vector_store = VectorStore(embedding_model=self.embedding_model, db_type=vector_store_type)
        self.chunk_strategy = chunk_strategy
    
    def index_pdf(self, pdf_path: str, persist_directory: Optional[str] = None, additional_metadata: Dict[str, Any] = None):
        """Index a PDF document into a vector store"""
        # Parse the PDF
        parser = PDFParser()
        parser.open(pdf_path)

        # Extract text and metadata
        text = parser.extract_all_text()
        cleaned_text = parser.clean_text(text)
        doc_metadata = parser.extract_metadata()

        # Close the parser
        parser.close()

        # Prepare metadata
        metadata = {
            "source": pdf_path,
            "title": doc_metadata.get("title", os.path.basename(pdf_path)),
            "author": doc_metadata.get("author", "Unknown"),
            "created_date": doc_metadata.get("creationDate", "Unknown"),
        }

        # Add any additional metadata
        if additional_metadata:
            metadata.update(additional_metadata)

        # Process and chunk the document
        chunks = self.processor.process_document(
            cleaned_text,
            metadata=metadata,
            chunk_strategy=self.chunk_strategy
        )

        # Store in vector database
        self.vector_store.create_from_documents(chunks, persist_directory=persist_directory)

        return {
            "documents": os.path.basename(pdf_path),
            "chunks": len(chunks),
            "status": "indexed"
        }