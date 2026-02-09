"""
Unified Pipeline for I-AURA-MED2D

Orchestrates all agents to provide end-to-end medical image analysis.
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

from ..agents.segmentation_agent import SegmentationAgent
from ..agents.router_agent import RouterAgent
from ..agents.report_agent import ReportAgent
from ..agents.reasoning_agent import ReasoningAgent
from ..agents.validation_agent import ValidationAgent
from .workflow_manager import WorkflowManager


class I_AURA_MED2D_Pipeline:
    """
    Main pipeline orchestrator for I-AURA-MED2D.
    
    Coordinates all agents to provide:
    1. Image segmentation
    2. Intelligent model routing
    3. Report generation
    4. Reasoning and Q&A
    5. Knowledge graph validation
    """
    
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the unified pipeline.
        
        Args:
            config: Configuration dictionary for all agents
            logger: Optional logger instance
        """
        self.config = config or {}
        self.logger = logger or self._setup_logger()
        self.workflow_manager = WorkflowManager()
        
        # Initialize agents
        self.segmentation_agent = None
        self.router_agent = None
        self.report_agent = None
        self.reasoning_agent = None
        self.validation_agent = None
        
        self._initialize_agents()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up logger for the pipeline."""
        logger = logging.getLogger("I_AURA_MED2D_Pipeline")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _initialize_agents(self):
        """Initialize all agents."""
        agent_configs = self.config.get('agents', {})
        
        # Segmentation Agent
        self.segmentation_agent = SegmentationAgent(
            config=agent_configs.get('segmentation', {}),
            logger=self.logger
        )
        
        # Router Agent
        self.router_agent = RouterAgent(
            config=agent_configs.get('router', {}),
            logger=self.logger
        )
        
        # Report Agent
        self.report_agent = ReportAgent(
            config=agent_configs.get('report', {}),
            logger=self.logger
        )
        
        # Reasoning Agent
        self.reasoning_agent = ReasoningAgent(
            config=agent_configs.get('reasoning', {}),
            logger=self.logger
        )
        
        # Validation Agent
        self.validation_agent = ValidationAgent(
            config=agent_configs.get('validation', {}),
            logger=self.logger
        )
        
        self.logger.info("All agents initialized")
    
    def process(
        self,
        image: Any,
        modality: Optional[str] = None,
        user_query: Optional[str] = None,
        enable_reasoning: bool = True,
        enable_validation: bool = True
    ) -> Dict[str, Any]:
        """
        Process medical image through the complete pipeline.
        
        Args:
            image: Medical image (numpy array, PIL Image, or file path)
            modality: Optional imaging modality (auto-detected if not provided)
            user_query: Optional question for reasoning agent
            enable_reasoning: Whether to run reasoning agent
            enable_validation: Whether to run validation agent
            
        Returns:
            Dictionary containing complete pipeline results:
                - 'segmentation': Segmentation results
                - 'routing': Routing decision
                - 'report': Generated report
                - 'reasoning': Reasoning results (if enabled)
                - 'validation': Validation results (if enabled)
                - 'metadata': Pipeline metadata
        """
        start_time = datetime.now()
        workflow_id = self.workflow_manager.create_workflow()
        
        try:
            self.logger.info(f"Starting pipeline processing (workflow: {workflow_id})")
            
            # Step 1: Segmentation
            self.logger.info("Step 1: Segmentation")
            segmentation_input = {
                'image': image,
                'modality': modality or 'unknown'
            }
            segmentation_result = self.segmentation_agent.execute(segmentation_input)
            
            if segmentation_result['_metadata']['status'] != 'success':
                raise RuntimeError("Segmentation failed")
            
            # Step 2: Routing
            self.logger.info("Step 2: Model Routing")
            routing_input = {
                'labels': segmentation_result.get('labels', []),
                'modality': segmentation_result.get('modality', 'unknown'),
                'body_regions': segmentation_result.get('body_regions', [])
            }
            routing_result = self.router_agent.execute(routing_input)
            
            if routing_result['_metadata']['status'] != 'success':
                raise RuntimeError("Routing failed")
            
            selected_model = routing_result.get('selected_model', 'BiomedGPT')
            
            # Step 3: Report Generation
            self.logger.info("Step 3: Report Generation")
            report_input = {
                'image': image,
                'labels': segmentation_result.get('labels', []),
                'modality': segmentation_result.get('modality', 'unknown'),
                'body_regions': segmentation_result.get('body_regions', []),
                'selected_model': selected_model
            }
            report_result = self.report_agent.execute(report_input)
            
            if report_result['_metadata']['status'] != 'success':
                raise RuntimeError("Report generation failed")
            
            # Step 4: Reasoning (optional)
            reasoning_result = None
            if enable_reasoning:
                self.logger.info("Step 4: Reasoning")
                reasoning_input = {
                    'image': image,
                    'report': report_result,
                    'question': user_query,
                    'task': 'qa' if user_query else 'explain'
                }
                reasoning_result = self.reasoning_agent.execute(reasoning_input)
            
            # Step 5: Validation (optional)
            validation_result = None
            if enable_validation:
                self.logger.info("Step 5: Validation")
                validation_input = {
                    'report': report_result,
                    'labels': segmentation_result.get('labels', []),
                    'modality': segmentation_result.get('modality', 'unknown')
                }
                validation_result = self.validation_agent.execute(validation_input)
            
            # Compile results
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                'segmentation': {
                    'masks': segmentation_result.get('masks', []),
                    'labels': segmentation_result.get('labels', []),
                    'confidences': segmentation_result.get('confidences', []),
                    'body_regions': segmentation_result.get('body_regions', [])
                },
                'routing': {
                    'selected_model': selected_model,
                    'confidence': routing_result.get('confidence', 0.0),
                    'reason': routing_result.get('reason', '')
                },
                'report': report_result,
                'reasoning': reasoning_result,
                'validation': validation_result,
                'metadata': {
                    'workflow_id': workflow_id,
                    'processing_time': processing_time,
                    'modality': segmentation_result.get('modality', 'unknown'),
                    'timestamp': datetime.now().isoformat(),
                    'pipeline_version': '0.1.0'
                }
            }
            
            self.workflow_manager.complete_workflow(workflow_id, 'success')
            self.logger.info(f"Pipeline completed successfully in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}")
            self.workflow_manager.complete_workflow(workflow_id, 'error', str(e))
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get pipeline status."""
        return {
            'agents': {
                'segmentation': self.segmentation_agent.get_status() if self.segmentation_agent else None,
                'router': self.router_agent.get_status() if self.router_agent else None,
                'report': self.report_agent.get_status() if self.report_agent else None,
                'reasoning': self.reasoning_agent.get_status() if self.reasoning_agent else None,
                'validation': self.validation_agent.get_status() if self.validation_agent else None
            },
            'workflows': self.workflow_manager.get_statistics()
        }

