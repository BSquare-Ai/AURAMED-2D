#!/usr/bin/env python3
"""
Setup HuggingFace authentication for BiomedGPT

This script helps you authenticate with HuggingFace to access BiomedGPT models.
"""

import subprocess
import sys

def main():
    print("=" * 60)
    print("HuggingFace Authentication Setup for BiomedGPT")
    print("=" * 60)
    
    print("\nTo use BiomedGPT from HuggingFace, you need to:")
    print("1. Have a HuggingFace account (create at https://huggingface.co/join)")
    print("2. Accept the model terms")
    print("3. Authenticate with HuggingFace CLI")
    
    print("\n" + "=" * 60)
    print("Step 1: Install HuggingFace CLI (if not already installed)")
    print("=" * 60)
    print("Run: pip install huggingface_hub[cli]")
    
    print("\n" + "=" * 60)
    print("Step 2: Login to HuggingFace")
    print("=" * 60)
    print("Run: huggingface-cli login")
    print("Enter your HuggingFace token (get it from https://huggingface.co/settings/tokens)")
    
    print("\n" + "=" * 60)
    print("Step 3: Accept Model Terms")
    print("=" * 60)
    print("Visit and accept terms for:")
    print("  - https://huggingface.co/PanaceaAI/BiomedGPT-base")
    print("  - https://huggingface.co/PanaceaAI/BiomedGPT-medium")
    print("  - https://huggingface.co/PanaceaAI/BiomedGPT-tiny")
    
    print("\n" + "=" * 60)
    print("Alternative: Use Local Checkpoints")
    print("=" * 60)
    print("If you have BiomedGPT checkpoints locally:")
    print("1. Download from: https://www.dropbox.com/sh/cu2r5zkj2r0e6zu/AADZ-KHn-emsICawm9CM4MqVa?dl=0")
    print("2. Update configs/pipeline_config.yaml:")
    print("   agents:")
    print("     reasoning:")
    print("       biomedgpt_path: \"/path/to/checkpoint\"")
    
    print("\n" + "=" * 60)
    print("Current Status")
    print("=" * 60)
    
    # Check if huggingface-cli is available
    try:
        result = subprocess.run(['huggingface-cli', 'whoami'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ Logged in as: {result.stdout.strip()}")
        else:
            print("✗ Not logged in to HuggingFace")
            print("  Run: huggingface-cli login")
    except:
        print("⚠ HuggingFace CLI not found")
        print("  Install: pip install huggingface_hub[cli]")
    
    print("\nNote: The demo will work with fallback implementation even without BiomedGPT")
    print("      BiomedGPT provides enhanced reasoning but is optional.")

if __name__ == "__main__":
    main()

