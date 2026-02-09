#!/usr/bin/env python3
"""
Download RRG models from HuggingFace

Downloads the RRG (Radiology Report Generation) models for chest X-ray report generation.
"""

import os
from pathlib import Path
from transformers import VisionEncoderDecoderModel, BertTokenizer, ViTImageProcessor
import torch

# Model configurations
RRG_MODELS = {
    'chexpert_mimic_findings': 'IAMJB/chexpert-mimic-cxr-findings-baseline',
    'chexpert_mimic_impression': 'IAMJB/chexpert-mimic-cxr-impression-baseline',
    'mimic_findings': 'IAMJB/mimic-cxr-findings-baseline',
    'mimic_impression': 'IAMJB/mimic-cxr-impression-baseline',
}

def download_model(model_name: str, model_id: str, save_dir: Path):
    """Download a single RRG model."""
    print(f"\nDownloading {model_name} from {model_id}...")
    save_path = save_dir / model_name
    
    try:
        # Download model
        print(f"  Downloading model...")
        model = VisionEncoderDecoderModel.from_pretrained(model_id)
        model.save_pretrained(save_path)
        
        # Download tokenizer
        print(f"  Downloading tokenizer...")
        tokenizer = BertTokenizer.from_pretrained(model_id)
        tokenizer.save_pretrained(save_path)
        
        # Download image processor
        print(f"  Downloading image processor...")
        image_processor = ViTImageProcessor.from_pretrained(model_id)
        image_processor.save_pretrained(save_path)
        
        print(f"  ✓ Successfully downloaded {model_name}")
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to download {model_name}: {e}")
        return False

def main():
    """Download all RRG models."""
    project_root = Path(__file__).parent.parent
    models_dir = project_root / "models" / "rrg"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Downloading RRG Models from HuggingFace")
    print("=" * 60)
    
    # Download default model (chexpert-mimic for both findings and impression)
    print("\nDownloading default RRG model (chexpert-mimic-impression)...")
    success = download_model(
        'default',
        RRG_MODELS['chexpert_mimic_impression'],
        models_dir
    )
    
    if success:
        print("\n✓ RRG model download completed!")
        print(f"  Model saved to: {models_dir / 'default'}")
    else:
        print("\n✗ RRG model download failed!")
        print("  You can download models manually using:")
        print("  from transformers import VisionEncoderDecoderModel")
        print(f"  model = VisionEncoderDecoderModel.from_pretrained('{RRG_MODELS['chexpert_mimic_impression']}')")
    
    print("\nNote: To download additional models, modify this script or run:")
    print("  python scripts/download_rrg.py")

if __name__ == "__main__":
    main()

