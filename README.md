# Customer Support Ticket Processor

An intelligent customer support ticket processing system implementing four key agentic design patterns.

## Patterns Implemented

1. **Prompt Chaining**: Preprocessing → Classification → Response Generation
2. **Routing**: Technical, Billing, General, and Complaint branches
3. **Parallelization**: Concurrent sentiment analysis, keyword extraction, priority scoring
4. **Reflection**: Self-improvement with iterative refinement

## Setup

1. Install Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Get API key from https://openrouter.ai/keys
4. Add to `.env`: `OPENROUTER_API_KEY=your-key`
5. Run: `python main.py`

## Git Flow

- `main`: Stable production code
- `develop`: Active development branch
- Feature branches: Created from `develop`

## Output Example
Processing Ticket #1
Original: hi my app keeps crashing...

PROMPT CHAINING
Cleaned: Hello, my app keeps crashing...
Category: technical

ROUTING
Branch: TECHNICAL

PARALLELIZATION
Priority: high

REFLECTION
Iteration 1: Score 7
Iteration 2: Score 8
FINAL RESPONSE: [Improved response]