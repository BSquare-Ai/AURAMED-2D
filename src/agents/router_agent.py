#!/usr/bin/env python3
"""
Router Agent for I-AURA-MED2D Pipeline

FINAL DESIGN (DEMO / EVALUATION SAFE):
- Router ALWAYS selects RRG for report generation
- BioMedGPT is used ONLY by ReasoningAgent
"""

from typing import Dict, Any, Optional
import torch
from .base_agent import BaseAgent


class RouterAgent(BaseAgent):
    """
    RouterAgent decides which REPORTING model to use.
    RRG is the ONLY valid report generator in this pipeline.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__("RouterAgent", config, logger)

        self.device = self._safe_device(self.config.get("device"))
        self.logger.info(f"RouterAgent initialized on {self.device} (RRG-forced mode)")

    def _safe_device(self, requested: Optional[str]) -> str:
        if requested == "mps" and torch.backends.mps.is_available():
            return "mps"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ALWAYS route to RRG for report generation.
        """

        self.logger.info(
            "Routing Decision: RRG | "
            "Report Generator: RRG | "
            "Reasoning: BioMedGPT (cloud) | "
            "Labels: CheXpert"
        )

        return {
            "selected_model": "RRG",
            "confidence": 1.0,
            "reason": "RRG is the dedicated radiology report generator",
            "device": self.device
        }
