from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
import re
import uuid

class DocumentProcessor:
    def __init__(self):
        pass

    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200, metadata: Dict[str, Any] = None) -> List[Document]:
        """Chunk text into smaller pieces for processing"""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        chunks = splitter.create_documents([text], [metadata or {}])
        return chunks