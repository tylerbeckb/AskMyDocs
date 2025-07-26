import pytest
import os
import tempfile
from src.data.loader import DocumentLoader
from langchain.schema import Document

class TestDocumentLoader:
    def test_init(self):
        """Test DocumentLoader initialisation with custom parameters"""
        loader = DocumentLoader(chunk_size=500, chunk_overlap=100)
        assert loader.chunk_size == 500
        assert loader.chunk_overlap == 100
    
    def test_file_not_found(self):
        """Test handling of non-existent file"""
        loader = DocumentLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_pdf("non_existent_file.pdf")

    def test_load_pdf(self, monkeypatch):
        """Test loading a PDF file with mocked PyPDFLoader"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_file:
            # Mock the PyPDFLoader. load method
            class MockPyPDFLoader:
                def __init__(self, file_path):
                    self.file_path = file_path

                def load(self):
                    return [
                        Document(page_content="Test content page 1", metadata={"page": 1}),
                        Document(page_content="Test content page 2", metadata={"page": 2})
                    ]
            # Patch the PyPDFLoader import in loader.py
            monkeypatch.setattr("src.data.loader.PyPDFLoader", MockPyPDFLoader)

            loader = DocumentLoader(chunk_size=1000, chunk_overlap=0)
            chunks = loader.load_pdf(temp_file.name)
            
            # Verify chunks were created
            assert len(chunks) > 0
            assert isinstance(chunks[0], Document)