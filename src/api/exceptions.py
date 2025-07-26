class DocumentProcessingError(Exception):
    """Raised when there is an error in processing a document."""
    pass

class VectorStoreError(Exception):
    """Raised when there is an error with the vector store."""
    pass

class DocumentNotFoundError(Exception):
    """Raised when a requested document is not found."""
    pass

class LLMError(Exception):
    """Raised when there is an error with the LLM service."""
    pass