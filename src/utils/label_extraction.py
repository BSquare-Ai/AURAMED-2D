"""
Label Extraction Utilities for I-AURA-MED2D Pipeline

Functions for extracting and normalizing anatomical labels from segmentation results.
"""

from typing import List, Dict, Set
import re


# Standard anatomical label mappings
ANATOMICAL_LABEL_MAP = {
    # Chest/Thorax
    'lung': ['lung', 'lungs', 'pulmonary', 'pneumonia'],
    'heart': ['heart', 'cardiac', 'myocardium'],
    'rib': ['rib', 'ribs', 'ribcage'],
    'chest': ['chest', 'thorax', 'thoracic'],
    
    # Abdomen
    'liver': ['liver', 'hepatic'],
    'spleen': ['spleen', 'splenic'],
    'kidney': ['kidney', 'renal', 'kidneys'],
    'kidney_right': ['kidney_right', 'right_kidney', 'right renal'],
    'kidney_left': ['kidney_left', 'left_kidney', 'left renal'],
    'pancreas': ['pancreas', 'pancreatic'],
    'stomach': ['stomach', 'gastric'],
    'intestine': ['intestine', 'bowel', 'intestinal'],
    
    # Pelvis
    'bladder': ['bladder', 'urinary'],
    'uterus': ['uterus', 'uterine'],
    'prostate': ['prostate', 'prostatic'],
    
    # Head
    'brain': ['brain', 'cerebral', 'cranial'],
    'skull': ['skull', 'cranium'],
    
    # Extremities
    'knee': ['knee', 'knees'],
    'hip': ['hip', 'hips', 'pelvic'],
    'wrist': ['wrist', 'wrists'],
    'shoulder': ['shoulder', 'shoulders'],
}


def extract_anatomical_labels(labels: List[str]) -> List[str]:
    """
    Extract anatomical structure labels from raw segmentation labels.
    
    Args:
        labels: List of raw labels from segmentation model
        
    Returns:
        List of normalized anatomical labels
    """
    normalized = []
    labels_lower = [label.lower() for label in labels]
    
    for label in labels_lower:
        # Try to match with known anatomical structures
        matched = False
        for standard_label, variants in ANATOMICAL_LABEL_MAP.items():
            if any(variant in label for variant in variants):
                if standard_label not in normalized:
                    normalized.append(standard_label)
                matched = True
                break
        
        # If no match, use original label (normalized)
        if not matched:
            clean_label = normalize_label(label)
            if clean_label not in normalized:
                normalized.append(clean_label)
    
    return normalized


def normalize_labels(labels: List[str]) -> List[str]:
    """
    Normalize a list of labels to standard format.
    
    Args:
        labels: List of labels to normalize
        
    Returns:
        List of normalized labels
    """
    return [normalize_label(label) for label in labels]


def normalize_label(label: str) -> str:
    """
    Normalize a single label to standard format.
    
    Args:
        label: Label string to normalize
        
    Returns:
        Normalized label string
    """
    # Convert to lowercase
    label = label.lower().strip()
    
    # Remove special characters (keep underscores and hyphens)
    label = re.sub(r'[^a-z0-9_\-\s]', '', label)
    
    # Replace spaces with underscores
    label = re.sub(r'\s+', '_', label)
    
    # Remove multiple underscores
    label = re.sub(r'_+', '_', label)
    
    # Remove leading/trailing underscores
    label = label.strip('_')
    
    return label


def get_body_region_from_labels(labels: List[str]) -> str:
    """
    Determine body region from anatomical labels.
    
    Args:
        labels: List of anatomical labels
        
    Returns:
        Detected body region (chest, abdomen, pelvis, head, extremity, or unknown)
    """
    labels_lower = [label.lower() for label in labels]
    
    region_keywords = {
        'chest': ['lung', 'heart', 'rib', 'chest', 'thorax'],
        'abdomen': ['liver', 'spleen', 'kidney', 'pancreas', 'stomach'],
        'pelvis': ['pelvis', 'bladder', 'uterus', 'prostate'],
        'head': ['brain', 'skull', 'head'],
        'extremity': ['knee', 'hip', 'wrist', 'shoulder', 'ankle', 'elbow']
    }
    
    for region, keywords in region_keywords.items():
        if any(keyword in label for label in labels_lower for keyword in keywords):
            return region
    
    return 'unknown'

