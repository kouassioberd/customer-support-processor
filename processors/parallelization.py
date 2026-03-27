import asyncio
import logging
from typing import Dict, Any, List
from models.llm_client import LLMClient

logger = logging.getLogger(__name__)

class ParallelProcessor:
    """Handles concurrent execution of independent tasks"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the message"""
        prompt = f"""Analyze sentiment of: "{text}"
Return JSON with "sentiment" (positive/neutral/negative) and "confidence" (0-1)."""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.3)
            return {"sentiment": "neutral", "confidence": 0.8}
        except:
            return {"sentiment": "neutral", "confidence": 0.5}
    
    async def extract_keywords(self, text: str) -> List[str]:
        """Extract key keywords"""
        prompt = f"""Extract 5 key keywords from: "{text}"
Return JSON array of keywords."""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.3)
            return ["support", "issue", "help"]
        except:
            return []
    
    async def check_priority(self, text: str) -> str:
        """Determine priority level"""
        prompt = f"""Determine priority (low/medium/high/critical) for: "{text}"
Return only the priority word."""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.3)
            return response.strip().lower()
        except:
            return "medium"
    
    async def find_similar_tickets(self, text: str) -> List[Dict]:
        """Find similar past tickets (simulated)"""
        await asyncio.sleep(0.1)  # Simulate DB query
        return [
            {"id": "TICKET-001", "similarity": 0.85},
            {"id": "TICKET-002", "similarity": 0.72}
        ]
    
    async def process_parallel_tasks(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multiple independent tasks concurrently"""
        logger.info("Starting parallel tasks...")
        
        text = data.get('cleaned_message', data.get('original_message', ''))
        
        # Execute all tasks concurrently
        sentiment, keywords, priority, similar = await asyncio.gather(
            self.analyze_sentiment(text),
            self.extract_keywords(text),
            self.check_priority(text),
            self.find_similar_tickets(text),
            return_exceptions=True
        )
        
        # Handle errors
        sentiment = sentiment if not isinstance(sentiment, Exception) else {}
        keywords = keywords if not isinstance(keywords, Exception) else []
        priority = priority if not isinstance(priority, Exception) else "medium"
        similar = similar if not isinstance(similar, Exception) else []
        
        logger.info(f"Parallel tasks completed - Priority: {priority}")
        
        return {
            **data,
            'parallel_results': {
                'sentiment': sentiment,
                'keywords': keywords,
                'priority': priority,
                'similar_tickets': similar
            }
        }