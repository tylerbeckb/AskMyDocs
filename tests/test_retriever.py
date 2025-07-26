import pytest
from unittest.mock import MagicMock
from src.rag.retriever import Retriever
from langchain.schema import Document

class TestRetriever:
    def test_init(self):
        """Test Retriever initialisation"""
        mock_vector_store = MagicMock()
        retriever = Retriever(vector_store=mock_vector_store)
        assert retriever.vector_store == mock_vector_store

    def test_retrieve(self):
        """Test Retriever initialisation"""
        # Create mock vector store with similarity search method
        mock_vector_store = MagicMock()
        mock_docs = [
            Document(page_content="Document 1", metadata={"source": "file1.pdf", "section": "COVERAGE"}),
            Document(page_content="Document 2", metadata={"source": "file1.pdf", "section": "EXCLUSIONS"})
        ]
        mock_vector_store.similarity_search.return_value = mock_docs

        # Create retriever with mock vector store
        retriever = Retriever(vector_store=mock_vector_store)

        # Test retrieve method
        result = retriever.retrieve("test query", top_k=2)

        # Verify the result
        assert len(result) == 2
        assert result[0].page_content == "Document 1"
        mock_vector_store.similarity_search.assert_called_once_with("test query", k=2)

    def test_format_context(self):
        """Test context formatting from documents"""
        mock_vector_store = MagicMock()
        retriever = Retriever(vector_store=mock_vector_store)
        docs = [
             Document(page_content="Test content 1", metadata={"source": "file1.pdf", "section": "COVERAGE"}),
            Document(page_content="Test content 2", metadata={"source": "file2.pdf", "section": "EXCLUSIONS"})
        ]

        context = retriever.format_context(docs)

        # Verify context formatting
        assert "file1.pdf" in context
        assert "file2.pdf" in context
        assert "COVERAGE" in context
        assert "EXCLUSIONS" in context
        assert "Test content 1" in context
        assert "Test content 2" in context