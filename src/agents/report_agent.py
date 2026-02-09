#!/usr/bin/env python3
"""
Report Agent for I-AURA-MED2D

FINAL DESIGN:
- Uses ONLY RRGModel for report generation
- NEVER calls BioMedGPT
- ALWAYS returns structured findings & impression
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.rrg_model import RRGModel


class ReportAgent(BaseAgent):
    def __init__(self, config=None, logger=None):
        super().__init__("ReportAgent", config, logger)

        # 🔑 LOCAL RRG MODEL (NOT BioMedGPT)
        self.rrg_model = RRGModel(
            model_path=config.get("rrg_path") if config else None,
            device=config.get("device", None) if config else None
        )

        self.logger.info("ReportAgent initialized with RRGModel")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, str]:
        """
        ALWAYS returns:
        {
            "findings": str,
            "impression": str
        }
        """

        try:
            image = input_data.get("image")
            if image is None:
                raise ValueError("No image provided to ReportAgent")

            # -------------------------
            # RRG GENERATION
            # -------------------------
            report_text = self.rrg_model.generate(image)

            # -------------------------
            # STRUCTURE ENFORCEMENT
            # -------------------------
            findings = ""
            impression = ""

            if "FINDINGS:" in report_text and "IMPRESSION:" in report_text:
                findings = report_text.split("FINDINGS:")[1].split("IMPRESSION:")[0].strip()
                impression = report_text.split("IMPRESSION:")[1].strip()
            else:
                findings = report_text.strip()
                impression = "Clinical correlation advised."

            return {
                "findings": findings,
                "impression": impression
            }

        except Exception as e:
            self.logger.error(f"RRG report generation failed: {e}")

            # ✅ SAFE, STRUCTURED FALLBACK
            return {
                "findings": "Unable to generate findings from the provided image.",
                "impression": "Please review the image manually."
            }
