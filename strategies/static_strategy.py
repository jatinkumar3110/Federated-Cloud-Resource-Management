"""
Static Strategy
Fixed allocation rules based on node type.

Simple baseline: allocate resources proportionally to node capacity.
"""

from typing import Dict, List
import numpy as np
from strategies.base_strategy import BaseStrategy
from simulation.node import Node


class StaticStrategy(BaseStrategy):
    """
    Static allocation: Fixed rules based on node capacity.
    
    Approach: Allocate CPU and memory proportionally to node's hardware capacity.
    - Edge device: 30% utilization
    - User device: 50% utilization
    - Compute server: 70% utilization
    - Data center: 80% utilization
    
    Advantage: No learning overhead, predictable, simple
    Disadvantage: Doesn't adapt to workload, ignores energy/SLA
    """
    
    # Allocation targets per node type
    ALLOCATION_TARGETS = {
        "edge_device": 0.30,
        "user_device": 0.50,
        "compute_server": 0.70,
        "data_center_node": 0.80
    }
    
    def __init__(self):
        """Initialize static strategy."""
        super().__init__("Static Allocation")
    
    def allocate_resources(self, nodes: List[Node]) -> Dict[int, Dict[str, float]]:
        """
        Allocate resources using fixed rules.
        
        Args:
            nodes: List of nodes
            
        Returns:
            Dictionary mapping node_id -> {cpu, memory} percentages
        """
        allocation = {}
        
        for node in nodes:
            if not node.is_available():
                allocation[node.node_id] = {"cpu": 0, "memory": 0}
                continue
            
            # Get target utilization for this node type
            node_type = node.node_type.value
            target_utilization = self.ALLOCATION_TARGETS.get(node_type, 0.5)
            
            # Convert to percentage
            cpu_percent = target_utilization * 100.0
            memory_percent = target_utilization * 100.0
            
            allocation[node.node_id] = {
                "cpu": float(cpu_percent),
                "memory": float(memory_percent)
            }
        
        return allocation
