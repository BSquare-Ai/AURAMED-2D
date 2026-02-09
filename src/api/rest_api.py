"""
REST API for I-AURA-MED2D Pipeline

Provides HTTP endpoints for accessing the pipeline.
"""

from typing import Optional
from flask import Flask, request, jsonify
import yaml
from pathlib import Path

from ..pipeline.unified_pipeline import I_AURA_MED2D_Pipeline


def create_app(config_path: Optional[str] = None) -> Flask:
    """
    Create Flask application.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "configs" / "pipeline_config.yaml"
    
    config = {}
    if Path(config_path).exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    
    # Initialize pipeline
    pipeline = I_AURA_MED2D_Pipeline(config=config)
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'pipeline': 'I-AURA-MED2D'
        })
    
    @app.route('/process', methods=['POST'])
    def process():
        """
        Process medical image through pipeline.
        
        Request body:
            - image: Image file or path
            - modality: Optional modality type
            - user_query: Optional question
            - enable_reasoning: Enable reasoning (default: true)
            - enable_validation: Enable validation (default: true)
        """
        try:
            data = request.json or {}
            
            # Extract parameters
            image = data.get('image')
            modality = data.get('modality')
            user_query = data.get('user_query')
            enable_reasoning = data.get('enable_reasoning', True)
            enable_validation = data.get('enable_validation', True)
            
            if image is None:
                return jsonify({'error': 'Image is required'}), 400
            
            # Process
            result = pipeline.process(
                image=image,
                modality=modality,
                user_query=user_query,
                enable_reasoning=enable_reasoning,
                enable_validation=enable_validation
            )
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/status', methods=['GET'])
    def status():
        """Get pipeline status."""
        try:
            status = pipeline.get_status()
            return jsonify(status), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app


def setup_routes(app: Flask):
    """
    Set up additional routes.
    
    Args:
        app: Flask application instance
    """
    # Additional routes can be added here
    pass


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

