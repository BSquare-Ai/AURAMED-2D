#!/usr/bin/env python3
"""
Load sample image from IMIS dataset

Helper script to load and prepare sample images from IMIS-Bench dataset.
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np

def find_imis_images(dataset_path=None, max_images=5):
    """
    Find sample images from IMIS dataset.
    
    Args:
        dataset_path: Path to IMIS dataset
        max_images: Maximum number of images to return
        
    Returns:
        List of image paths
    """
    if dataset_path is None:
        # Try common locations
        possible_paths = [
            Path("/home/ajaid/IMIS-Bench/dataset"),
            Path("/home/ajaid/IMIS-Bench/demo_image"),
            Path(__file__).parent.parent.parent / "IMIS-Bench" / "dataset"
        ]
        
        for path in possible_paths:
            if path.exists():
                dataset_path = path
                break
    
    if dataset_path is None:
        print("IMIS dataset not found. Please specify dataset_path.")
        return []
    
    dataset_path = Path(dataset_path)
    image_paths = []
    
    # Search for common image formats
    image_extensions = ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.nii', '.nii.gz']
    
    # Look in image subdirectories
    for ext in image_extensions:
        if ext in ['.nii', '.nii.gz']:
            continue  # Skip NIfTI for now
        pattern = f"**/*{ext}"
        found = list(dataset_path.glob(pattern))[:max_images]
        image_paths.extend(found)
        if len(image_paths) >= max_images:
            break
    
    return image_paths[:max_images]


def load_sample_image(image_path):
    """
    Load and preprocess a sample image.
    
    Args:
        image_path: Path to image file
        
    Returns:
        PIL Image
    """
    image_path = Path(image_path)
    
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    # Load image
    try:
        image = Image.open(image_path)
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    
    except Exception as e:
        raise RuntimeError(f"Failed to load image: {e}")


if __name__ == "__main__":
    # Find sample images
    print("Searching for IMIS dataset images...")
    images = find_imis_images()
    
    if images:
        print(f"\nFound {len(images)} sample images:")
        for img_path in images:
            print(f"  - {img_path}")
    else:
        print("\nNo images found. You can:")
        print("1. Place sample images in IMIS-Bench/dataset/")
        print("2. Use the demo_image directory")
        print("3. Upload your own images through the UI")

