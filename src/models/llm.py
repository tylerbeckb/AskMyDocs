from langchain_core.language_models.llms import BaseLLM
import os 
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, ClassVar
from langchain_core.outputs import LLMResult, Generation
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from pydantic import Field, PrivateAttr

load_dotenv()

class DeepSeekLLM(BaseLLM):
    """Custom LLM class for DeepSeek API"""
    
    model_name: str = Field(default="deepseek-chat")
    temperature: float = Field(default=0.0)
    
    _api_key: str = PrivateAttr()
    _api_url: str = PrivateAttr(default="https://api.deepseek.com/v1/chat/completions")

    def __init__(self, model_name="deepseek-chat", temperature=0.0, api_key=None, **kwargs):
        # Initialize with Pydantic fields
        super().__init__(model_name=model_name, temperature=temperature, **kwargs)
        
        # Set private attributes
        self._api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self._api_key:
            raise ValueError("DeepSeek API key is required")
        self._api_url = "https://api.deepseek.com/v1/chat/completions"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, 
              run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs) -> str:
        """Process a text prompt and return a completion"""
        messages = [{"role": "user", "content": prompt}]
        return self._generate_response(messages)
    
    def _generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate a response from the DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature
        }

        response = requests.post(self._api_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise ValueError(f"Error from DeepSeek API: {response.text}")
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs
    ) -> LLMResult:
        """Generate text from a list of prompts."""
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
            generations.append([Generation(text=text)])
        return LLMResult(generations=generations)
    
    @property
    def _llm_type(self) -> str:
        return "deepseek"


class LLMService:
    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.0):
        self.model_name = model_name
        self.temperature = temperature
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