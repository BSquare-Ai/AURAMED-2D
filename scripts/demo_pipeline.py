#!/usr/bin/env python3
"""
Demo script for I-AURA-MED2D Pipeline

Demonstrates basic usage of the unified pipeline.
"""

import sys
from pathlib import Path
import yaml

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from pipeline.unified_pipeline import I_AURA_MED2D_Pipeline


def main():
    """Run demo pipeline."""
    print("I-AURA-MED2D Pipeline Demo")
    print("=" * 50)
    
    # Load configuration
    config_path = project_root / "configs" / "pipeline_config.yaml"
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}
        print("Warning: Config file not found, using defaults")
    
    # Initialize pipeline
    print("\nInitializing pipeline...")
    pipeline = I_AURA_MED2D_Pipeline(config=config)
    print("Pipeline initialized successfully!")
    
    # Example: Process a medical image
    # Note: Replace with actual image path
    image_path = "path/to/medical/image.png"
    
    print(f"\nProcessing image: {image_path}")
    print("Note: This is a demo. Replace with actual image path to test.")
    
    # Uncomment to run actual processing:
    # try:
    #     result = pipeline.process(
    #         image=image_path,
    #         modality='xray',
    #         user_query='What are the key findings?',
    #         enable_reasoning=True,
    #         enable_validation=True
    #     )
    #     
    #     print("\nResults:")
    #     print(f"Labels: {result['segmentation']['labels']}")
    #     print(f"Selected Model: {result['routing']['selected_model']}")
    #     print(f"Report Findings: {result['report']['findings'][:200]}...")
    #     print(f"Validation: {result['validation']['is_valid']}")
    #     
    # except Exception as e:
    #     print(f"Error: {e}")
    
    # Get pipeline status
    print("\nPipeline Status:")
    status = pipeline.get_status()
    print(f"Active workflows: {status['workflows']['active_workflows']}")
    print(f"Total workflows: {status['workflows']['total']}")
    
    print("\nDemo completed!")


if __name__ == "__main__":
    main()

