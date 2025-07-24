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