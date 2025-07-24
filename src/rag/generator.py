from src.models.llm import LLMService
from src.rag.retriever import Retriever
from typing import Dict, Any, Optional, List

class AnswerGenerator:
    def __init__(self, retriever: Retriever, llm_service: LLMService):
        self.retriever = retriever
        self.llm_service = llm_service

        # Default system prompt for travel insurance queries
        self.system_prompt = """
        You are an AI assistant specializing in travel insurance policies.
        Your task is to provide accurate information based solely on the provided context.
        If the answer is not in the context, say "I don't have enough information to answer this question."
        Do not make up or infer information that is not explicitly stated in the context.
        Format your responses clearly and concisely.
        """

    def generate_answer(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """Generate an answer for the given query"""
        # Retrive relevant documents
        retrieved_docs = self.retriever.retrieve(query, top_k=top_k)

        # If not docuemnts are retrieved, return a default message
        if not retrieved_docs:
            return {
                "answer": "I don't have enough information to answer this question.",
                "sources": [],
                "context": "",
            }
        
        # Format the retrieved documents into context
        context = self.retriever.format_context(retrieved_docs)

        # Generate the answer using the LLM service
        answer = self.llm_service.generate_with_context(
            self.system_prompt,
            context,
            query
        )

        # Extract sources
        sources = [
            {
                "source": doc.metadata.get("source", "Unknown"),
                "section": doc.metadata.get("section", "General")
            }
            for doc in retrieved_docs
        ]

        return {
            "answer": answer,
            "sources": sources,
            "context": context
        }
    
    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt for the LLM"""
        self.system_prompt = prompt