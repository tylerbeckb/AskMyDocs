from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List, Optional, Dict, Any

class LLMService:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temparture: float = 0.0):
        self.model_name = model_name
        self.temperature = temparture
        self.llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using the OpenAI API"""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        try:
            response = self.llm(messages)
            return response.content
        except Exception as e:
            raise RuntimeError(f"Error generating response: {str(e)}")
        