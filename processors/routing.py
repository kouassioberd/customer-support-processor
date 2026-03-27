import logging
from typing import Dict, Any
from models.llm_client import LLMClient

logger = logging.getLogger(__name__)

class RoutingProcessor:
    """Handles routing to specialized branches based on ticket category"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    async def process_technical(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Technical issue branch"""
        prompt = f"""Generate troubleshooting steps for this technical issue:

Issue: {data.get('classification', {}).get('entities', {}).get('issue_type')}
Message: {data.get('cleaned_message')}

Provide step-by-step troubleshooting instructions."""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.5)
            return {
                "branch": "technical",
                "response": f"Technical Support:\n{response}"
            }
        except Exception as e:
            logger.error(f"Technical processing failed: {e}")
            return {
                "branch": "technical",
                "response": "Our technical team will investigate this issue."
            }
    
    async def process_billing(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Billing branch"""
        prompt = f"""Handle this billing inquiry:

Message: {data.get('cleaned_message')}

Provide policy information and next steps."""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.5)
            return {
                "branch": "billing",
                "response": f"Billing Support:\n{response}"
            }
        except Exception as e:
            logger.error(f"Billing processing failed: {e}")
            return {
                "branch": "billing",
                "response": "Our billing team will review your request."
            }
    
    async def process_general(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """General inquiry branch"""
        prompt = f"""Answer this general inquiry:

Message: {data.get('cleaned_message')}

Provide helpful information."""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.7)
            return {
                "branch": "general",
                "response": f"General Support:\n{response}"
            }
        except Exception as e:
            logger.error(f"General processing failed: {e}")
            return {
                "branch": "general",
                "response": "Thank you for your inquiry."
            }
    
    async def process_complaint(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Complaint branch"""
        prompt = f"""Handle this complaint with empathy:

Message: {data.get('cleaned_message')}

Provide empathetic response and escalation plan."""

        try:
            response = await self.llm.generate_async(prompt, temperature=0.7)
            return {
                "branch": "complaint",
                "response": f"Senior Support:\n{response}",
                "escalation_required": True
            }
        except Exception as e:
            logger.error(f"Complaint processing failed: {e}")
            return {
                "branch": "complaint",
                "response": "We sincerely apologize. A senior agent will contact you.",
                "escalation_required": True
            }
    
    async def route(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate branch"""
        category = processed_data.get('classification', {}).get('category', 'general')
        
        logger.info(f"Routing to branch: {category}")
        
        branch_handlers = {
            'technical': self.process_technical,
            'billing': self.process_billing,
            'general': self.process_general,
            'complaint': self.process_complaint
        }
        
        handler = branch_handlers.get(category, self.process_general)
        branch_result = await handler(processed_data)
        
        return {**processed_data, **branch_result, 'routing_decision': category}