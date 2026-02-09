#!/usr/bin/env python3
"""
BioMedGPT Cloud Model Wrapper
--------------------------------
Client used in the local (Cursor) pipeline to communicate
with a BioMedGPT reasoning model running on Google Colab
via FastAPI + ngrok.

Architecture:
Local Pipeline → HTTP POST → Colab FastAPI → BioMedGPT → Answer
"""

import os
import requests
from typing import Optional


class BiomedGPTModel:
    """
    Lightweight HTTP client for BioMedGPT running on Colab.
    """

    def __init__(self, api_url: Optional[str] = None, timeout: int = 60):
        """
        Parameters
        ----------
        api_url : str, optional
            Public ngrok URL exposing the Colab FastAPI `/infer` endpoint.
            Example:
            https://xxxxxx.ngrok-free.dev/infer

        timeout : int
            Request timeout in seconds.
        """

        # Priority:
        # 1. Explicit argument
        # 2. Environment variable
        # 3. Hardcoded fallback (demo-safe)
        self.api_url = (
            api_url
            or os.getenv("BIOMEDGPT_API_URL")
            or "https://nonspatially-behavioristic-santana.ngrok-free.dev/infer"
        )

        if not self.api_url.endswith("/infer"):
            raise ValueError(
                "BioMedGPT API URL must end with `/infer`"
            )

        self.timeout = timeout
        self.model_name = "BioMedGPT-7B (Colab Cloud)"

        print(f"✓ {self.model_name} client initialized")
        print(f"✓ Endpoint: {self.api_url}")

    def answer_question(self, question: str, context: str = "") -> str:
        """
        Sends a clinical question + radiology report context
        to the BioMedGPT Cloud API.

        Parameters
        ----------
        question : str
            User's clinical question (MCQ or free-text).

        context : str
            Radiology report text (RRG output).

        Returns
        -------
        str
            Grounded clinical answer from BioMedGPT.
        """

        if not question or question.strip() == "":
            return "No clinical question provided."

        if not context or context.strip() == "":
            return "No radiology report provided."

        payload = {
            "report_text": context,
            "user_query": question
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

            if "answer" not in data:
                return "BioMedGPT Cloud returned an invalid response."

            return data["answer"]

        except requests.exceptions.Timeout:
            return (
                "BioMedGPT Cloud timeout. "
                "The model may be warming up — please try again shortly."
            )

        except requests.exceptions.ConnectionError:
            return (
                "Unable to reach BioMedGPT Cloud. "
                "Please ensure Colab and ngrok are running."
            )

        except requests.exceptions.HTTPError as e:
            return (
                f"BioMedGPT Cloud HTTP error: {str(e)}"
            )

        except Exception as e:
            return (
                f"BioMedGPT Cloud unexpected error: {str(e)}"
            )
