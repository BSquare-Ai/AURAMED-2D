"""
Base Agent Class for I-AURA-MED2D Agentic Framework

All agents inherit from this base class to ensure consistent interface,
error handling, logging, and communication patterns.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from datetime import datetime
import traceback


class BaseAgent(ABC):
    """
    Base class for all agents in the I-AURA-MED2D pipeline.
    
    Provides common functionality:
    - Processing interface
    - Validation
    - Error handling
    - Logging
    - Communication with other agents
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name/identifier
            config: Agent-specific configuration dictionary
            logger: Optional logger instance (creates one if not provided)
        """
        self.name = name
        self.config = config or {}
        self.logger = logger or self._setup_logger()
        self.status = "initialized"
        self.last_error = None
        self.processing_history = []
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logger for the agent."""
        logger = logging.getLogger(f"{self.__class__.__name__}.{self.name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        Args:
            input_data: Dictionary containing input data for processing
            
        Returns:
            Dictionary containing processing results
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement process() method")
    
    def validate(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the output of processing.
        
        Args:
            output: Output dictionary to validate
            
        Returns:
            Dictionary with validation results:
            {
                'is_valid': bool,
                'errors': List[str],
                'warnings': List[str],
                'confidence': float
            }
        """
        errors = []
        warnings = []
        confidence = 1.0
        
        # Basic validation: check if output is a dictionary
        if not isinstance(output, dict):
            errors.append("Output must be a dictionary")
            confidence = 0.0
        
        # Check for required keys (subclasses can override)
        required_keys = self._get_required_output_keys()
        for key in required_keys:
            if key not in output:
                errors.append(f"Missing required key: {key}")
                confidence = max(0.0, confidence - 0.2)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'confidence': confidence
        }
    
    def _get_required_output_keys(self) -> List[str]:
        """
        Get list of required output keys for validation.
        Override in subclasses to specify required keys.
        """
        return []
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent with error handling and logging.
        
        Args:
            input_data: Input data for processing
            
        Returns:
            Dictionary containing results and metadata
        """
        start_time = datetime.now()
        self.status = "processing"
        self.last_error = None
        
        try:
            self.logger.info(f"{self.name} starting processing")
            
            # Process input
            result = self.process(input_data)
            
            # Validate output
            validation = self.validate(result)
            
            # Add metadata
            result['_metadata'] = {
                'agent_name': self.name,
                'status': 'success' if validation['is_valid'] else 'validation_failed',
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'validation': validation,
                'timestamp': datetime.now().isoformat()
            }
            
            if not validation['is_valid']:
                self.logger.warning(
                    f"{self.name} validation failed: {validation['errors']}"
                )
            
            self.status = "completed"
            self.processing_history.append({
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'processing_time': result['_metadata']['processing_time']
            })
            
            self.logger.info(f"{self.name} completed successfully")
            return result
            
        except Exception as e:
            self.status = "error"
            self.last_error = str(e)
            error_trace = traceback.format_exc()
            
            self.logger.error(f"{self.name} failed: {str(e)}")
            self.logger.debug(error_trace)
            
            self.processing_history.append({
                'timestamp': datetime.now().isoformat(),
                'status': 'error',
                'error': str(e)
            })
            
            return {
                '_metadata': {
                    'agent_name': self.name,
                    'status': 'error',
                    'error': str(e),
                    'error_trace': error_trace,
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'timestamp': datetime.now().isoformat()
                }
            }
    
    def communicate(self, message: Dict[str, Any], target_agent: Optional[str] = None) -> Dict[str, Any]:
        """
        Communicate with other agents or the pipeline orchestrator.
        
        Args:
            message: Message dictionary
            target_agent: Optional target agent name
            
        Returns:
            Response dictionary
        """
        self.logger.debug(f"{self.name} sending message to {target_agent or 'orchestrator'}")
        return {
            'from': self.name,
            'to': target_agent,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status."""
        return {
            'name': self.name,
            'status': self.status,
            'last_error': self.last_error,
            'processing_count': len(self.processing_history),
            'recent_history': self.processing_history[-5:] if self.processing_history else []
        }
    
    def reset(self):
        """Reset agent state."""
        self.status = "initialized"
        self.last_error = None
        self.processing_history = []
        self.logger.info(f"{self.name} reset")

