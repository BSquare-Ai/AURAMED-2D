#!/usr/bin/env python3
"""
Setup BiomedGPT

Sets up BiomedGPT by creating symlinks and checking dependencies.
"""

import os
import sys
from pathlib import Path
import subprocess

def check_biomedgpt():
    """Check if BiomedGPT is available."""
    # Check multiple possible locations
    possible_paths = [
        Path("/home/ajaid/BiomedGPT"),
        Path(__file__).parent.parent.parent / "BiomedGPT",
        Path(__file__).parent.parent / "BiomedGPT"
    ]
    
    for biomedgpt_path in possible_paths:
        if biomedgpt_path.exists():
            print(f"✓ BiomedGPT found at {biomedgpt_path}")
            return True, biomedgpt_path
    
    # Not found
    print(f"✗ BiomedGPT not found in any expected location")
    print("  Please ensure BiomedGPT is cloned:")
    print("  cd /home/ajaid && git clone https://github.com/taokz/BiomedGPT.git")
    return False, None

def check_requirements(biomedgpt_path):
    """Check if BiomedGPT requirements are installed."""
    requirements_file = biomedgpt_path / "requirements.txt"
    
    if not requirements_file.exists():
        print("⚠ BiomedGPT requirements.txt not found")
        return False
    
    print("✓ BiomedGPT requirements.txt found")
    return True

def install_requirements(biomedgpt_path):
    """Install BiomedGPT requirements."""
    requirements_file = biomedgpt_path / "requirements.txt"
    
    if not requirements_file.exists():
        print("⚠ Cannot install requirements - requirements.txt not found")
        return False
    
    print("\nInstalling BiomedGPT requirements...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True
        )
        print("✓ BiomedGPT requirements installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def create_symlink(biomedgpt_path):
    """Create symlink to BiomedGPT in models directory."""
    project_root = Path(__file__).parent.parent
    models_dir = project_root / "models" / "biomedgpt"
    
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Create symlink
    symlink_path = models_dir / "BiomedGPT"
    
    if symlink_path.exists() or symlink_path.is_symlink():
        print(f"✓ Symlink already exists: {symlink_path}")
        return True
    
    try:
        symlink_path.symlink_to(biomedgpt_path)
        print(f"✓ Created symlink: {symlink_path} -> {biomedgpt_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to create symlink: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("Setting up BiomedGPT")
    print("=" * 60)
    
    # Check if BiomedGPT exists
    found, biomedgpt_path = check_biomedgpt()
    if not found:
        return
    
    # Check requirements
    check_requirements(biomedgpt_path)
    
    # Ask user if they want to install requirements
    print("\nDo you want to install BiomedGPT requirements? (y/n)")
    print("Note: This may take some time and install additional packages.")
    # For automation, we'll skip the prompt and just create symlink
    # response = input().strip().lower()
    # if response == 'y':
    #     install_requirements(biomedgpt_path)
    
    # Create symlink
    create_symlink(biomedgpt_path)
    
    print("\n" + "=" * 60)
    print("BiomedGPT Setup Complete")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Install BiomedGPT requirements (if needed):")
    print("   cd /home/ajaid/BiomedGPT && pip install -r requirements.txt")
    print("2. Download BiomedGPT checkpoints (see BiomedGPT repository)")
    print("3. Update configs/pipeline_config.yaml with model paths")

if __name__ == "__main__":
    main()

