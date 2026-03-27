#!/usr/bin/env python3
"""
Customer Support Ticket Processor
Implements Prompt Chaining, Routing, Parallelization, and Reflection patterns
"""

import asyncio
import logging
import sys
from colorama import init, Fore, Style
from config import LOG_LEVEL, LOG_FILE
from models.llm_client import LLMClient
from processors.prompt_chaining import PromptChainProcessor
from processors.routing import RoutingProcessor
from processors.parallelization import ParallelProcessor
from processors.reflection import ReflectionProcessor
from utils.logger import setup_logging
from utils.data_loader import load_test_data

init(autoreset=True)

# Setup logging
setup_logging(LOG_LEVEL, LOG_FILE)
logger = logging.getLogger(__name__)

class SupportTicketProcessor:
    """Main orchestrator for the support ticket processing pipeline"""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.chain_processor = PromptChainProcessor(self.llm_client)
        self.routing_processor = RoutingProcessor(self.llm_client)
        self.parallel_processor = ParallelProcessor(self.llm_client)
        self.reflection_processor = ReflectionProcessor(self.llm_client)
    
    def print_section(self, title: str, color=Fore.CYAN):
        print(f"\n{color}{'='*80}")
        print(f"{color}{title}")
        print(f"{color}{'='*80}{Style.RESET_ALL}")
    
    async def process_ticket(self, ticket: dict, index: int) -> dict:
        """Process a single support ticket"""
        print(f"\n{Fore.YELLOW}{'─'*80}")
        print(f"{Fore.YELLOW}Processing Ticket #{index + 1}")
        print(f"{Fore.YELLOW}{'─'*80}{Style.RESET_ALL}")
        
        raw_message = ticket.get('message', '')
        print(f"{Fore.WHITE}Original: {raw_message}{Style.RESET_ALL}")
        
        # Step 1: Prompt Chaining
        self.print_section("1. PROMPT CHAINING")
        chain_result = await self.chain_processor.process_chain(raw_message)
        print(f"   Cleaned: {chain_result['cleaned_message'][:100]}...")
        print(f"   Category: {chain_result['classification'].get('category')}")
        
        # Step 2: Routing
        self.print_section("2. ROUTING")
        routed_result = await self.routing_processor.route(chain_result)
        print(f"   Branch: {routed_result.get('routing_decision', 'unknown').upper()}")
        
        # Step 3: Parallelization
        self.print_section("3. PARALLELIZATION")
        parallel_result = await self.parallel_processor.process_parallel_tasks(routed_result)
        parallel_data = parallel_result.get('parallel_results', {})
        print(f"   Priority: {parallel_data.get('priority', 'medium')}")
        print(f"   Keywords: {parallel_data.get('keywords', [])[:3]}")
        
        # Step 4: Reflection
        self.print_section("4. REFLECTION")
        final_result = await self.reflection_processor.reflect_and_improve(parallel_result)
        
        # Show reflection improvements
        history = final_result.get('reflection_history', [])
        if history:
            for h in history:
                print(f"   Iteration {h['iteration']}: Score {h.get('score', 'N/A')}")
        
        print(f"\n{Fore.MAGENTA}FINAL RESPONSE:")
        print(f"{Fore.WHITE}{final_result.get('final_response', 'No response')}")
        
        return final_result
    
    async def run_pipeline(self, test_data: list):
        """Run the complete pipeline"""
        print(f"\n{Fore.CYAN}{'█'*80}")
        print(f"{Fore.CYAN} CUSTOMER SUPPORT TICKET PROCESSOR")
        print(f"{Fore.CYAN} Patterns: Prompt Chaining | Routing | Parallelization | Reflection")
        print(f"{Fore.CYAN}{'█'*80}{Style.RESET_ALL}")
        
        results = []
        for i, ticket in enumerate(test_data):
            try:
                result = await self.process_ticket(ticket, i)
                results.append(result)
                print(f"\n{Fore.GREEN}✓ Ticket #{i+1} processed{Style.RESET_ALL}")
            except Exception as e:
                logger.error(f"Failed: {e}")
                print(f"{Fore.RED}✗ Ticket #{i+1} failed{Style.RESET_ALL}")
        
        # Summary
        self.print_section("SUMMARY", Fore.CYAN)
        print(f"Processed: {len(results)}/{len(test_data)} tickets")
        
        return results

async def main():
    """Main entry point"""
    try:
        test_tickets = load_test_data()
        processor = SupportTicketProcessor()
        results = await processor.run_pipeline(test_tickets)
        
        print(f"\n{Fore.GREEN}✅ Pipeline completed!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed: {e}")
        print(f"\n{Fore.RED}❌ Failed: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())