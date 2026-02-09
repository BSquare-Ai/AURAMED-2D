"""
Report Formatting Utilities for I-AURA-MED2D Pipeline

Functions for formatting and standardizing radiology reports.
"""

from typing import Dict, Any, Optional
import re


def format_report(
    findings: str,
    impression: str,
    model_used: str,
    confidence: Optional[float] = None,
    uncertainties: Optional[list] = None,
    key_entities: Optional[list] = None
) -> Dict[str, Any]:
    """
    Format a radiology report into standardized structure.
    
    Args:
        findings: Findings section text
        impression: Impression section text
        model_used: Name of model used for generation
        confidence: Confidence score (0-1)
        uncertainties: List of uncertain findings
        key_entities: List of key medical entities mentioned
        
    Returns:
        Dictionary with standardized report structure
    """
    return {
        'findings': findings.strip(),
        'impression': impression.strip(),
        'model_used': model_used,
        'confidence': confidence,
        'uncertainties': uncertainties or [],
        'key_entities': key_entities or [],
        'format': 'standard'
    }


def standardize_report(report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standardize a report to ensure consistent format.
    
    Args:
        report: Report dictionary (may have various formats)
        
    Returns:
        Standardized report dictionary
    """
    standardized = {
        'findings': '',
        'impression': '',
        'model_used': report.get('model_used', 'unknown'),
        'confidence': report.get('confidence'),
        'uncertainties': report.get('uncertainties', []),
        'key_entities': report.get('key_entities', []),
        'format': 'standard'
    }
    
    # Extract findings
    if 'findings' in report:
        standardized['findings'] = str(report['findings']).strip()
    elif 'report' in report:
        # Try to split report into findings and impression
        text = str(report['report'])
        standardized['findings'], standardized['impression'] = split_report(text)
    
    # Extract impression
    if 'impression' in report:
        standardized['impression'] = str(report['impression']).strip()
    elif 'conclusion' in report:
        standardized['impression'] = str(report['conclusion']).strip()
    
    return standardized


def split_report(report_text: str) -> tuple:
    """
    Split a report text into findings and impression sections.
    
    Args:
        report_text: Full report text
        
    Returns:
        Tuple of (findings, impression)
    """
    # Common section headers
    findings_keywords = ['findings:', 'observation:', 'description:']
    impression_keywords = ['impression:', 'conclusion:', 'summary:']
    
    text_lower = report_text.lower()
    
    # Find impression section
    impression_start = -1
    for keyword in impression_keywords:
        idx = text_lower.find(keyword)
        if idx != -1:
            impression_start = idx
            break
    
    if impression_start != -1:
        findings = report_text[:impression_start].strip()
        impression = report_text[impression_start:].strip()
        # Remove header from impression
        for keyword in impression_keywords:
            if impression.lower().startswith(keyword):
                impression = impression[len(keyword):].strip()
                break
    else:
        # No clear split, use entire text as findings
        findings = report_text
        impression = ''
    
    return findings, impression


def extract_entities_from_report(report_text: str) -> list:
    """
    Extract medical entities from report text (simple keyword-based).
    
    Args:
        report_text: Report text
        
    Returns:
        List of potential medical entities
    """
    # This is a simple implementation
    # In production, use NER models or knowledge graph matching
    
    common_entities = [
        'pneumonia', 'fracture', 'mass', 'lesion', 'nodule',
        'effusion', 'edema', 'atelectasis', 'cardiomegaly',
        'pneumothorax', 'consolidation', 'opacity'
    ]
    
    found_entities = []
    text_lower = report_text.lower()
    
    for entity in common_entities:
        if entity in text_lower:
            found_entities.append(entity)
    
    return found_entities

