#!/usr/bin/env python3
"""
Run I-AURA-MED2D Demo Application (Hybrid-Cloud Version)
Optimized for MacBook Air M4. 
"""

import sys
import os
import subprocess
from pathlib import Path
import yaml

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Force HF Token into Environment (REPLACE WITH YOUR TOKEN)
os.environ["HF_TOKEN"] = "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" 

try:
    from src.demo.demo_app import create_demo_ui
except ImportError as e:
    print(f"❌ Error: Missing components in src/demo/. Check imports: {e}")
    sys.exit(1)

def kill_port(port):
    """Forcefully clear the port if it's being held by a stale process."""
    try:
        # Mac command to find and kill process on a port
        subprocess.run(f"lsof -ti:{port} | xargs kill -9", shell=True, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def main():
    print("=" * 60)
    print("      I-AURA-MED2D: MEDICAL IMAGING PIPELINE (M4)")
    print("=" * 60)
    
    # 1. Load configuration
    config_path = project_root / "configs" / "pipeline_config.yaml"
    config = {}
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print("✓ Configuration loaded from pipeline_config.yaml")
    else:
        print("⚠ Configuration file not found! Falling back to defaults.")
        config = {'agents': {}}

    # 2. Hybrid-Cloud Health Check
    print("\n[System Check]")
    # Verify token
    token = os.getenv("HF_TOKEN")
    if not token or token == "your_actual_token_here":
        print("❌ ERROR: HF_TOKEN is missing or not set in run_demo.py!")
        print("   Please edit run_demo.py and paste your token from hf.co/settings/tokens")
        sys.exit(1)
    else:
        print(f"✓ Cloud Reasoning Ready (Token: {token[:4]}***{token[-4:]})")
    
    # 3. Port Cleanup
    target_port = 7860
    print(f"✓ Cleaning up port {target_port}...")
    kill_port(target_port)

    # 4. Create and Launch Demo
    print("\nInitializing demo application...")
    try:
        demo = create_demo_ui(config)
        
        print("\n" + "=" * 60)
        print("Launching Gradio UI...")
        print("=" * 60)
        print(f"\nInterface running on: http://127.0.0.1:{target_port}")
        print("Press Ctrl+C to safely shut down the server.\n")
        
        demo.launch(
            server_name="127.0.0.1",
            server_port=target_port,
            share=False,
            show_error=True
        )
    except Exception as e:
        print(f"❌ Failed to launch UI: {e}")

if __name__ == "__main__":
    main()