import aiohttp
import asyncio
from typing import List, Dict, Any
import logging
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME, TIMEOUT_SECONDS

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with LLM APIs with async support"""
    
    def __init__(self, model: str = MODEL_NAME):
        self.model = model
        self.base_url = OPENROUTER_BASE_URL
        self.api_key = OPENROUTER_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_async(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """Generate response asynchronously"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            try:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        logger.error(f"API Error {response.status}: {error_text}")
                        return f"Error: {response.status}"
            except asyncio.TimeoutError:
                logger.error("Request timeout")
                return "Error: Timeout"
            except Exception as e:
                logger.error(f"Request failed: {e}")
                return f"Error: {str(e)}"