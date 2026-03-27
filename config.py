import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Set to True to use mock responses (for testing without API)
# Set to False to use real API with free models
USE_MOCK_MODE = False  # ← CHANGE THIS TO False to use real API

# Free models available on OpenRouter (use exact names from docs)
# All of these are confirmed working as of March 2026:
AVAILABLE_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",  # Fast, good throughput
    "qwen/qwen3-next-80b-a3b-instruct:free",   # Good reasoning
    "openai/gpt-oss-20b:free",                 # Fastest, good for simple tasks
    "z-ai/glm-4.5-air:free"                   # Good for long context
]

# Select the model to use (try different ones if one fails)
MODEL_NAME = "nvidia/nemotron-3-super-120b-a12b:free"  # Start with this one

# Pipeline configuration
MAX_REFLECTION_ITERATIONS = 2
TIMEOUT_SECONDS = 60

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/pipeline.log"