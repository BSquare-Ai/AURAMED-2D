#!/usr/bin/env python3
"""
Reasoning Agent for I-AURA-MED2D Pipeline

STRICT DESIGN:
- BioMedGPT is used ONLY for question answering
- Input is TEXT ONLY (RRG-generated report)
- No images, masks, labels, or segmentation metadata
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.biomedgpt_model import BiomedGPTModel


class ReasoningAgent(BaseAgent):
    """
    Agent responsible for clinical reasoning and QA
    based strictly on RRG-generated radiology reports.
    """

    def __init__(self, config: Dict[str, Any], logger=None):
        super().__init__("ReasoningAgent", config, logger)

        # --------------------------------------------------
        # 🔑 Validate configuration
        # --------------------------------------------------
        if not isinstance(config, dict):
            raise ValueError("ReasoningAgent config must be a dictionary")

        if "api_url" not in config:
            raise ValueError(
                "ReasoningAgent requires 'api_url' in config "
                "(BioMedGPT FastAPI /infer endpoint)"
            )

        self.api_url = config["api_url"]

        # --------------------------------------------------
        # 🔗 Initialize BioMedGPT HTTP client
        # --------------------------------------------------
        self.model = BiomedGPTModel(api_url=self.api_url)

        if self.logger:
            self.logger.info("ReasoningAgent initialized successfully")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform grounded clinical reasoning using BioMedGPT.

        Expected input_data format:
        {
            "report": str | {
                "findings": str,
                "impression": str
            },
            "question": str
        }
        """

        try:
            # -----------------------------
            # 1. Extract inputs
            # -----------------------------
            if not isinstance(input_data, dict):
                raise ValueError("input_data must be a dictionary")

            report = input_data.get("report", "")
            question = input_data.get("question", "")

            if not isinstance(question, str) or not question.strip():
                raise ValueError("No clinical question provided to ReasoningAgent")

            question = question.strip()

            # -----------------------------
            # 2. Normalize report STRICTLY
            # -----------------------------
            if isinstance(report, dict):
                findings = report.get("findings", "").strip()
                impression = report.get("impression", "").strip()
                report_text = f"{findings}\n\n{impression}".strip()
            else:
                report_text = str(report).strip()

            if not report_text:
                raise ValueError("Empty report text passed to ReasoningAgent")

            # -----------------------------
            # 3. HARD SAFETY CHECKS
            # -----------------------------
            assert isinstance(report_text, str)
            assert isinstance(question, str)

            # -----------------------------
            # 4. Call BioMedGPT (TEXT ONLY)
            # -----------------------------
            answer = self.model.answer_question(
                question=question,
                context=report_text
            )

            return {
                "answer": str(answer),
                "confidence": 0.9,
                "reasoning": "BioMedGPT clinical QA based on RRG-generated report"
            }

        except Exception as e:
            if self.logger:
                self.logger.warning(f"ReasoningAgent failed: {e}")

            return {
                "answer": "Clinical reasoning temporarily unavailable.",
                "confidence": 0.5,
                "reasoning": "Reasoning error"
            }
