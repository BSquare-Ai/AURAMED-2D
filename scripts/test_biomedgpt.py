#!/usr/bin/env python3
"""
Test if BioMedGPT is being used by the reasoning agent (Cloud Version).
Updated for MacBook Air M4 to verify Hugging Face API connectivity.
"""

import sys
from pathlib import Path
import yaml

# 1. Setup paths to find your src directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.agents.reasoning_agent import ReasoningAgent
except ImportError:
    print("❌ Error: Could not find ReasoningAgent. Ensure you are running from the project root.")
    sys.exit(1)

def main():
    print("=" * 60)
    print("Testing BioMedGPT Integration (Cloud API)")
    print("=" * 60)
    
    # Load config
    config_path = project_root / "configs" / "pipeline_config.yaml"
    if not config_path.exists():
        print(f"❌ Error: Config file not found at {config_path}")
        return
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print("\n1. Initializing Reasoning Agent...")
    try:
        # Initialize the agent with your reasoning config
        agent = ReasoningAgent(config=config['agents']['reasoning'])
        print(f"✅ Agent initialized using: {config['agents']['reasoning'].get('biomedgpt_path', 'default')}")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    print("\n2. Checking Model Connection Status:")
    if agent.model is None:
        print("   ❌ Model wrapper is missing!")
        print("   Status: Using fallback implementation.")
        return

    # Check if the model wrapper is pointing to the Cloud Inference Client
    # We check for the 'client' attribute instead of 'model' or 'processor'
    is_cloud = hasattr(agent.model, 'client')
    print(f"   Model wrapper type: {type(agent.model).__name__}")
    print(f"   Cloud API connection: {'Active' if is_cloud else 'Not Found (Check your biomedgpt_model.py)'}")

    print("\n3. Performing Live Reasoning Test...")
    test_context = "Findings: Left lower lobe consolidation with air bronchograms. No pleural effusion."
    test_query = "What is the most likely diagnosis?"
    
    try:
        # We call the agent's answer_question method
        # This will trigger the cloud API call
        print(f"   Sending query to BioMedGPT...")
        response = agent.model.answer_question(image_path=None, question=test_query)
        
        if response and "answer" in response and response.get("confidence", 0) > 0:
            print("\n✅ YES - Reasoning agent IS using BioMedGPT Cloud!")
            print(f"   Model: {getattr(agent.model, 'model_name', 'BioMedGPT-7B')}")
            print(f"   Sample Response: {response['answer'][:100]}...")
        else:
            print("\n❌ NO - Reasoning agent returned an invalid or fallback response.")
            print(f"   Debug Data: {response}")
            
    except Exception as e:
        print(f"\n❌ ERROR during API call: {e}")
        print("   Check your internet connection and Hugging Face Token.")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()