import pytest
from unittest.mock import MagicMock
from src.rag.generator import AnswerGenerator
from src.models.llm import LLMService
from src.rag.retriever import Retriever
from langchain.schema import Document

class TestAnswerGenerator:
    def setup_method(self):
        """Set up test fixtures for each test method"""
        self.mock_retriever = MagicMock(spec=Retriever)
        self.mock_llm_service = MagicMock(spec=LLMService)
        self.answer_generator = AnswerGenerator(
            retriever=self.mock_retriever,
            llm_service=self.mock_llm_service
        )

    def test_init(self):
        """Test AnswerGenerator initialisation"""
        assert self.answer_generator.retriever == self.mock_retriever
        assert self.answer_generator.llm_service == self.mock_llm_service
        assert isinstance(self.generator.system_prompt, str)
        assert len(self.generator.system_prompt) > 0

    def test_generate_answer_with_docs(self):
        """Test answer generation with retrieved documents"""
        # Mock retriever.retrieve to return documents
        mock_docs = [
            Document(page_content="Test content", metadata={"source": "file.pdf", "section": "COVERAGE"})
        ]
        self.mock_retriever.retrieve.return_value = mock_docs

        # Mock format_context
        self.mock_retriever.format_context.return_value = "Formatted context"

        # Mock LLM service response
        self.mock_llm_service.generate_with_context.return_value = "Generated answer"

        # Generate answer
        result = self.generator.generate_answer("test query")

        # Verify result
        assert result["answer"] == "Generated answer"
        assert len(result["sources"]) == 1
        assert result["sources"][0]["source"] == "file.pdf"

        # Verify method calls
        self.mock_retriever.retrieve.assert_called_once_with("test query", top_k=3)
        self.mock_llm_service.generate_with_context.assert_called_once()

    def test_generate_answer_no_docs(self):
        """Test answer generation with no retrieved documents"""
        # Mock retriever.retrieve to return empty list
        self.mock_retriever.retrieve.return_value = []

        # Generate answer
        result = self.generator.generate_answer("test query")

        # Verify result
        assert "don't have enough information" in result["answer"]
        assert result["sources"] == []

        # Verify LLM was not called
        self.mock_llm_service.generate_with_context.assert_not_called()

    def test_set_system_prompt(self):
        """Test setting a custom system prompt"""
        new_prompt = "New system prompt"
        self.generator.set_system_prompt(new_prompt)
        assert self.generator.system_prompt == new_prompt