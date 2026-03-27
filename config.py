import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Free models available on OpenRouter
MODEL_NAME = "openai/gpt-oss-20b:free"  # Can change to any free model
# Alternative free models:
# "qwen/qwen3-next-80b-a3b-instruct:free"
# "nvidia/nemotron-3-super-120b-a12b:free"
# "z-ai/glm-4.5-air:free"

# Pipeline configuration
MAX_REFLECTION_ITERATIONS = 2
TIMEOUT_SECONDS = 60

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/pipeline.log"