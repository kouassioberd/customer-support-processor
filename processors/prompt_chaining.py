import json
import logging
from typing import Dict, Any
from models.llm_client import LLMClient

logger = logging.getLogger(__name__)

class PromptChainProcessor:
    """Handles sequential prompt chaining for ticket processing"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    async def preprocess(self, raw_message: str) -> Dict[str, Any]:
        """Step 1: Clean and normalize raw user message"""
        prompt = f"""You are a preprocessing assistant. Clean and normalize the following customer support message.

Task:
1. Fix typos and grammar errors
2. Expand common abbreviations (e.g., "pls" -> "please", "thx" -> "thanks")
3. Standardize format (proper capitalization, punctuation)

Return a JSON object with:
- "cleaned_text": the normalized message
- "corrections_made": list of corrections you made

Raw message: "{raw_message}"

Response format (JSON only):"""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.3)
            # Extract JSON from response
            result = json.loads(response.strip())
            logger.info(f"Preprocessing completed: {len(result.get('corrections_made', []))} corrections")
            return result
        except json.JSONDecodeError:
            logger.error("Failed to parse preprocessing response")
            return {"cleaned_text": raw_message, "corrections_made": []}
    
    async def classify(self, cleaned_text: str) -> Dict[str, Any]:
        """Step 2: Classify the ticket and extract key entities"""
        prompt = f"""You are a classification assistant. Analyze the following customer support message.

Tasks:
1. Determine ticket category: "technical", "billing", "general", or "complaint"
2. Extract key entities: product name, issue type, urgency (low/medium/high)

Message: "{cleaned_text}"

Return a JSON object with:
- "category": string
- "entities": {{"product": string, "issue_type": string, "urgency": string}}
- "sentiment": string
- "confidence": float (0-1)

Response format (JSON only):"""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.3)
            result = json.loads(response.strip())
            logger.info(f"Classification: {result.get('category')}, Confidence: {result.get('confidence')}")
            return result
        except json.JSONDecodeError:
            logger.error("Failed to parse classification response")
            return {
                "category": "general",
                "entities": {"product": "unknown", "issue_type": "unknown", "urgency": "medium"},
                "sentiment": "neutral",
                "confidence": 0.5
            }
    
    async def generate_draft(self, classification: Dict[str, Any], original_text: str) -> Dict[str, Any]:
        """Step 3: Generate initial draft response"""
        prompt = f"""You are a customer support agent. Generate a professional response.

Classification:
- Category: {classification.get('category')}
- Issue: {classification.get('entities', {}).get('issue_type')}
- Urgency: {classification.get('entities', {}).get('urgency')}

Customer: "{original_text}"

Return JSON with:
- "draft_response": the response text
- "tone": string

Response format (JSON only):"""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.7)
            result = json.loads(response.strip())
            logger.info("Draft response generated")
            return result
        except json.JSONDecodeError:
            logger.error("Failed to parse draft response")
            return {
                "draft_response": "Thank you for contacting support. We'll look into this and get back to you soon.",
                "tone": "professional"
            }
    
    async def process_chain(self, raw_message: str) -> Dict[str, Any]:
        """Execute the full prompt chain"""
        logger.info("Starting prompt chain...")
        
        # Step 1: Preprocess
        preprocessing_result = await self.preprocess(raw_message)
        cleaned_text = preprocessing_result.get('cleaned_text', raw_message)
        
        # Step 2: Classify
        classification = await self.classify(cleaned_text)
        
        # Step 3: Generate draft response
        draft = await self.generate_draft(classification, cleaned_text)
        
        logger.info("Prompt chain completed")
        
        return {
            "original_message": raw_message,
            "cleaned_message": cleaned_text,
            "corrections": preprocessing_result.get('corrections_made', []),
            "classification": classification,
            "draft_response": draft.get('draft_response', ''),
            "tone": draft.get('tone', 'professional')
        }