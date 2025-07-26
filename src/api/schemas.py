from pydantic import BaseModel, Field
from typing import Optional, List

class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's question about travel insurance")
    top_k: int = Field(default=3, description="Number of documents to retrieve")

class DocumentSource(BaseModel):
    source: str
    section: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[DocumentSource]

class DocumentUploadResponse(BaseModel):
    filename: str
    chunks: int
    status: str

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None