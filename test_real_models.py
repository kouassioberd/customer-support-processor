# test_real_models.py
import asyncio
import sys
from models.llm_client import LLMClient
from config import AVAILABLE_MODELS

async def test_model(model_name):
    """Test if a specific model works"""
    print(f"\n{'='*50}")
    print(f"Testing: {model_name}")
    print('='*50)
    
    client = LLMClient(model=model_name)
    
    # Simple test prompt
    test_prompt = "Say 'Hello! This model is working correctly.' in exactly one sentence."
    
    print("Sending request...")
    response = await client.generate_async(test_prompt, temperature=0.5)
    
    if "Error:" in response or "404" in response or "429" in response:
        print(f"❌ FAILED: {response[:100]}")
        return False
    else:
        print(f"✅ WORKING!")
        print(f"Response: {response[:200]}...")
        return True

async def main():
    print("\n" + "█"*60)
    print(" TESTING FREE MODELS ON OPENROUTER")
    print("█"*60)
    
    working_models = []
    
    for model in AVAILABLE_MODELS:
        if await test_model(model):
            working_models.append(model)
        await asyncio.sleep(2)  # Wait 2 seconds between tests
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Working models: {len(working_models)}/{len(AVAILABLE_MODELS)}")
    
    for model in working_models:
        print(f"  ✅ {model}")
    
    if working_models:
        print("\n🎯 Add this to your config.py:")
        print(f'MODEL_NAME = "{working_models[0]}"')
    else:
        print("\n⚠️ No models working. Check your API key or try again later.")
        print("You can still use mock mode: USE_MOCK_MODE = True")

if __name__ == "__main__":
    asyncio.run(main())