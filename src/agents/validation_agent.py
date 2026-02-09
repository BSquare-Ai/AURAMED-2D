#!/usr/bin/env python3
"""
Validation Agent for I-AURA-MED2D Pipeline.
Checks report consistency against segmentation labels and medical logic.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from .base_agent import BaseAgent

# These are likely local helper classes in your src/knowledge/ directory
try:
    from ..knowledge.umls_validator import UMLSValidator
    from ..knowledge.snomed_validator import SNOMEDValidator
    from ..knowledge.radgraph_validator import RadGraphValidator
except ImportError:
    # Fallback placeholders if knowledge modules aren't fully implemented
    UMLSValidator = SNOMEDValidator = RadGraphValidator = None

class ValidationAgent(BaseAgent):
    """
    Agent responsible for validating reports against medical knowledge.
    Ensures that what the AI 'sees' matches what the AI 'writes'.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__("ValidationAgent", config, logger)
        
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.validators = {}
        self._load_validators()
    
    def _load_validators(self):
        """Load knowledge graph validators if data files exist."""
        # We only load these if the classes were successfully imported
        configs = {
            'umls': (UMLSValidator, 'umls_path', "knowledge/data/umls"),
            'snomed': (SNOMEDValidator, 'snomed_path', "knowledge/data/snomed"),
            'radgraph': (RadGraphValidator, None, None)
        }

        for key, (cls, cfg_key, default_path) in configs.items():
            if cls is not None:
                try:
                    path = self.config.get(cfg_key) or str(self.project_root / default_path) if default_path else None
                    self.validators[key] = cls(path) if path else cls()
                    self.logger.info(f"✓ {key.upper()} validator loaded.")
                except Exception as e:
                    self.logger.warning(f"⚠ {key.upper()} Validator skipped: Data files not found.")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        report = input_data.get('report', {})
        labels = input_data.get('labels', [])
        
        # 1. Structural Validation
        findings = report.get('findings', '').lower()
        impression = report.get('impression', '').lower()
        report_text = findings + " " + impression

        results = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'confidence': 1.0
        }

        # 2. Anatomical Consistency (Crucial for M4 Local/Cloud Hybrid)
        # This checks if labels from the local segmenter are mentioned in the cloud report
        for label in labels:
            if label.lower() not in report_text:
                results['warnings'].append(f"Omission: '{label}' detected in image but not mentioned in report.")
                results['confidence'] -= 0.1

        # 3. Knowledge Graph Checks (If loaded)
        for name, validator in self.validators.items():
            val_res = validator.validate(report)
            if not val_res.get('is_valid', True):
                results['errors'].extend(val_res.get('errors', []))
                results['is_valid'] = False

        return results

    def _get_required_output_keys(self) -> List[str]:
        return ['is_valid', 'confidence']