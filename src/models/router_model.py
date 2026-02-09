import os

class SimpleRouter:
    """
    Intelligent Router for I-AURA-MED2D.
    Decides between Segmentation, Report Generation (RRG), and Complex Reasoning (BioMedGPT).
    """
    def __init__(self, config=None):
        self.config = config or {}
        # Keywords that trigger specific models
        self.rrg_keywords = ["report", "describe", "summarize", "findings", "impressions"]
        self.biomed_keywords = ["why", "explain", "mechanism", "research", "compare", "diagnose"]

    def route(self, task_type=None, user_query=""):
        """
        Logic to decide which agent handles the request.
        """
        # 1. If the user explicitly asks for a task type (e.g., from a button click)
        if task_type:
            return task_type

        # 2. Intelligent Routing based on text query
        query_lower = user_query.lower()

        if any(word in query_lower for word in self.biomed_keywords):
            return "biomedgpt"  # Routes to complex reasoning
            
        if any(word in query_lower for word in self.rrg_keywords):
            return "rrg"       # Routes to report generation

        # 3. Default Fallback
        return "segmentation"

class RouterModel(SimpleRouter):
    """Maintains backward compatibility with your existing ReasoningAgent."""
    pass