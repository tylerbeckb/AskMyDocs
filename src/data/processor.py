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
    
    def chunk_insurance_doc(self, text: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """Specialised chunking for insurance documents"""
        section_pattern = r'(?:^|\n)([A-Z][A-Z\s]+:)'

        # Find all sections
        sections = re.split(section_pattern, text)

        documents = []
        current_section = "GENERAL"

        # Process sections
        for i, section in enumerate(sections):
            # Content
            if i % 2 == 0 and i > 0:
                # Combine header and content
                section_text = sections[i-1] + section
                section_metadata = metadata.copy() if metadata else {}
                section_metadata["section"] = current_section
                section_metadata["chunk_id"] = str(uuid.uuid4())

                # Create document
                doc = Document(page_content=section_text, metadata=section_metadata)
                documents.append(doc)
            # Header
            elif i % 2 == 1:
                current_section = section.strip()
            
        return documents
    
    def enhance_metadata(self, documents: List[Document], additional_metadata: Dict[str, Any]) -> List[Document]:
        """Add additional metadata to all documents in the list"""
        for doc in documents:
            doc.metadata.update(additional_metadata)
        return documents