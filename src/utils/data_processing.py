"""
Data Processing Utilities for I-AURA-MED2D Pipeline

Functions for image preprocessing, normalization, and format conversion.
"""

import numpy as np
from typing import Union, Tuple, Optional
from PIL import Image
import cv2


def preprocess_image(
    image: Union[np.ndarray, str, Image.Image],
    target_size: Tuple[int, int] = (1024, 1024),
    normalize: bool = True
) -> np.ndarray:
    """
    Preprocess medical image for model input.
    
    Args:
        image: Input image (numpy array, file path, or PIL Image)
        target_size: Target size (height, width)
        normalize: Whether to normalize pixel values
        
    Returns:
        Preprocessed image as numpy array
    """
    # Load image if path provided
    if isinstance(image, str):
        image = Image.open(image)
    
    # Convert PIL to numpy
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    # Convert grayscale to RGB if needed
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
    # Resize image
    if image.shape[:2] != target_size:
        image = cv2.resize(image, (target_size[1], target_size[0]), 
                          interpolation=cv2.INTER_LINEAR)
    
    # Normalize if requested
    if normalize:
        image = normalize_image(image)
    
    return image


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image pixel values to [0, 1] range.
    
    Args:
        image: Input image array
        
    Returns:
        Normalized image array
    """
    if image.dtype == np.uint8:
        image = image.astype(np.float32) / 255.0
    elif image.max() > 1.0:
        image = image.astype(np.float32) / image.max()
    
    return image


def convert_to_tensor(image: np.ndarray) -> np.ndarray:
    """
    Convert image to tensor format (add batch dimension if needed).
    
    Args:
        image: Image array
        
    Returns:
        Tensor array with shape (1, H, W, C) or (1, C, H, W)
    """
    if len(image.shape) == 3:
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
    
    return image


def detect_modality(image_path: str) -> str:
    """
    Detect imaging modality from file path or metadata.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Detected modality string
    """
    path_lower = image_path.lower()
    
    modality_keywords = {
        'xray': ['xray', 'x-ray', 'chest', 'cxr'],
        'ct': ['ct', 'computed', 'tomography'],
        'mri': ['mri', 'magnetic', 'resonance'],
        'ultrasound': ['ultrasound', 'us', 'sono'],
        'endoscopy': ['endoscopy', 'endoscopic', 'scope']
    }
    
    for modality, keywords in modality_keywords.items():
        if any(keyword in path_lower for keyword in keywords):
            return modality
    
    return 'unknown'

