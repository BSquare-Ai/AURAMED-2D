#!/usr/bin/env python3
"""
Download RRG models from HuggingFace (Simple version using huggingface_hub)

Downloads the RRG models without requiring full model loading.
"""

import os
from pathlib import Path

try:
    from huggingface_hub import snapshot_download
except ImportError:
    print("Installing huggingface_hub...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub"])
    from huggingface_hub import snapshot_download

# Default model to download
DEFAULT_MODEL = 'IAMJB/chexpert-mimic-cxr-impression-baseline'

def main():
    """Download RRG model."""
    project_root = Path(__file__).parent.parent
    models_dir = project_root / "models" / "rrg" / "default"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Downloading RRG Model from HuggingFace")
    print("=" * 60)
    print(f"Model: {DEFAULT_MODEL}")
    print(f"Destination: {models_dir}")
    print()
    
    try:
        print("Downloading model files...")
        snapshot_download(
            repo_id=DEFAULT_MODEL,
            local_dir=str(models_dir),
            local_dir_use_symlinks=False
        )
        print(f"\n✓ Successfully downloaded RRG model to {models_dir}")
        print("\nModel files:")
        for file in sorted(models_dir.rglob("*")):
            if file.is_file():
                print(f"  - {file.relative_to(models_dir)}")
        
    except Exception as e:
        print(f"\n✗ Failed to download model: {e}")
        print("\nYou can download manually using:")
        print(f"  from huggingface_hub import snapshot_download")
        print(f"  snapshot_download('{DEFAULT_MODEL}', local_dir='{models_dir}')")

if __name__ == "__main__":
    main()

