"""
API Endpoints for I-AURA-MED2D Pipeline

RESTful API for accessing the pipeline:
- REST API: Standard HTTP endpoints
- Streaming API: Real-time streaming responses
"""

from .rest_api import create_app, setup_routes

__all__ = [
    "create_app",
    "setup_routes",
]

