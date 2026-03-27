import logging
from typing import Dict, Any, List
from models.llm_client import LLMClient

logger = logging.getLogger(__name__)

class ReflectionProcessor:
    """Handles self-improvement through reflection loops"""
    
    def __init__(self, llm_client: LLMClient, max_iterations: int = 2):
        self.llm = llm_client
        self.max_iterations = max_iterations
        self.reflection_history = []
    
    async def evaluate_response(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the quality of a response"""
        prompt = f"""Evaluate this support response (1-10 scale):

Response: {response}

Return JSON with "overall_score", "strengths" (list), "improvements" (list)."""

        try:
            # Simplified evaluation for demo
            return {
                "overall_score": 7,
                "strengths": ["Clear communication"],
                "improvements": ["Add specific next steps"]
            }
        except:
            return {
                "overall_score": 5,
                "strengths": [],
                "improvements": ["Needs improvement"]
            }
    
    async def improve_response(self, original_response: str, evaluation: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate improved version based on evaluation"""
        improvements = evaluation.get('improvements', [])
        improvements_text = "\n".join([f"- {imp}" for imp in improvements])
        
        prompt = f"""Improve this response:

Original: {original_response}

Areas to improve:
{improvements_text}

Provide improved version:"""

        try:
            improved = await self.llm.generate_async(prompt, temperature=0.7)
            return improved.strip()
        except:
            return original_response + " We're here to help."
    
    async def reflect_and_improve(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Main reflection loop"""
        logger.info("Starting reflection loop...")
        
        current_response = data.get('response', data.get('draft_response', ''))
        iteration = 0
        self.reflection_history = []
        
        while iteration < self.max_iterations:
            logger.info(f"Reflection iteration {iteration + 1}")
            
            # Evaluate
            evaluation = await self.evaluate_response(current_response, data)
            
            # Store history
            self.reflection_history.append({
                'iteration': iteration + 1,
                'score': evaluation.get('overall_score', 0),
                'improvements': evaluation.get('improvements', [])
            })
            
            # Check if good enough
            if evaluation.get('overall_score', 0) >= 8:
                logger.info(f"Score {evaluation['overall_score']} >= 8, stopping")
                break
            
            if not evaluation.get('improvements'):
                break
            
            # Improve
            current_response = await self.improve_response(current_response, evaluation, data)
            iteration += 1
        
        return {
            **data,
            'final_response': current_response,
            'reflection_history': self.reflection_history,
            'improvement_iterations': iteration
        }