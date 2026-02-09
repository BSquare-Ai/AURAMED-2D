"""
Workflow Manager for I-AURA-MED2D Pipeline

Manages workflow state and tracking across pipeline execution.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid
from collections import defaultdict


class WorkflowManager:
    """
    Manages workflow state and statistics.
    """
    
    def __init__(self):
        """Initialize workflow manager."""
        self.workflows = {}
        self.statistics = defaultdict(int)
    
    def create_workflow(self) -> str:
        """
        Create a new workflow.
        
        Returns:
            Workflow ID
        """
        workflow_id = str(uuid.uuid4())
        self.workflows[workflow_id] = {
            'id': workflow_id,
            'status': 'created',
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
            'error': None
        }
        self.statistics['total'] += 1
        return workflow_id
    
    def update_workflow(
        self,
        workflow_id: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Update workflow status.
        
        Args:
            workflow_id: Workflow ID
            status: New status
            metadata: Optional metadata to add
        """
        if workflow_id in self.workflows:
            self.workflows[workflow_id]['status'] = status
            if metadata:
                self.workflows[workflow_id].update(metadata)
    
    def complete_workflow(
        self,
        workflow_id: str,
        status: str = 'completed',
        error: Optional[str] = None
    ):
        """
        Mark workflow as completed.
        
        Args:
            workflow_id: Workflow ID
            status: Completion status
            error: Optional error message
        """
        if workflow_id in self.workflows:
            self.workflows[workflow_id]['status'] = status
            self.workflows[workflow_id]['completed_at'] = datetime.now().isoformat()
            if error:
                self.workflows[workflow_id]['error'] = error
            
            self.statistics[status] += 1
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Get workflow information.
        
        Args:
            workflow_id: Workflow ID
            
        Returns:
            Workflow dictionary or None
        """
        return self.workflows.get(workflow_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get workflow statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            'total': self.statistics['total'],
            'completed': self.statistics.get('completed', 0),
            'success': self.statistics.get('success', 0),
            'error': self.statistics.get('error', 0),
            'active_workflows': len([w for w in self.workflows.values() 
                                   if w['status'] not in ['completed', 'error']])
        }

