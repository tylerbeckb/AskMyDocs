from langchain_core.language_models.llms import BaseLLM
from typing import List, Dict
import os 
import requests
from dotenv import load_dotenv

load_dotenv()

class DeepSeekLLM(BaseLLM):
    """Custom LLM class for DeepSeek API"""

    def __init__(self, model_name="deepseek-chat", temperature=0.0, api_key=None):
        super().__init__()
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DeepSeek API key is required")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    def _call(self, prompt: str, **kwargs) -> str:
        """Process a text prompt and return a completion"""
        messages = [{"role": "user", "content": prompt}]
        return self._generate_response(messages)
    
    def _generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response from the DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise ValueError(f"Error from DeepSeek API: {response.text}")
        data = response.json()
        return data["choices"][0]["message"]["content"]


class LLMService:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temparture: float = 0.0):
        self.model_name = model_name
        self.temperature = temparture
        self.llm = DeepSeekLLM(model_name=self.model_name, temperature=self.temperature)

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using the DeepSeek API"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = self.llm._generate_response(messages)
            return response
        except Exception as e:
            raise RuntimeError(f"Error generating response: {str(e)}")
        
    def generate_with_context(self, system_prompt: str, context: str, query: str) -> str:
        """Generate a response with context"""
        user_prompt = f"Context information is below:\n{context}\n\nGiven the context, please answer the question: {query}"
        return self.generate_response(system_prompt, user_prompt)