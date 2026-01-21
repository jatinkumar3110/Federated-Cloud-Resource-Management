"""
Energy-Aware Heuristic Strategy
Simple rules based on energy efficiency and SLA.

Practical baseline that ignores ML entirely.
"""

from typing import Dict, List
import numpy as np
from strategies.base_strategy import BaseStrategy
from simulation.node import Node


class EnergyAwareStrategy(BaseStrategy):
    """
    Energy-aware heuristic allocation.
    
    Approach: Simple rules prioritizing energy-efficient nodes.
    - Rank nodes by energy efficiency
    - Allocate more to efficient nodes
    - Reduce allocation for high-SLA-sensitive nodes
    
    Advantage: Simple, no learning overhead, energy-focused
    Disadvantage: Ignores convergence, doesn't adapt to workload
    """
    
    def __init__(self):
        """Initialize energy-aware strategy."""
        super().__init__("Energy-Aware Heuristic")
    
    def allocate_resources(self, nodes: List[Node]) -> Dict[int, Dict[str, float]]:
        """
        Allocate resources using energy-aware heuristic.
        
        Args:
            nodes: List of nodes
            
        Returns:
            Dictionary mapping node_id -> {cpu, memory} percentages
        """
        allocation = {}
        
        # Rank nodes by energy efficiency
        available_nodes = [n for n in nodes if n.is_available()]
        
        if not available_nodes:
            return {n.node_id: {"cpu": 0, "memory": 0} for n in nodes}
        
        # Compute energy efficiency score for each node
        node_scores = []
        for node in available_nodes:
            # Efficiency = 1 / energy_cost_factor (lower cost = more efficient)
            energy_efficiency = 1.0 / (node.profile.energy_cost_factor + 1e-6)
            
            # Apply SLA sensitivity penalty
            sla_penalty = node.profile.sla_sensitivity * 0.2
            
            efficiency_score = energy_efficiency * (1.0 - sla_penalty)
            node_scores.append((node.node_id, node, efficiency_score))
        
        # Sort by efficiency (descending)
        node_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Allocate based on rank and efficiency
        for rank, (node_id, node, score) in enumerate(node_scores):
            # More efficient nodes get higher allocation
            # Normalize score and map to allocation percentage
            normalized_score = score / (max([s[2] for s in node_scores]) + 1e-6)
            
            # Base allocation increases with efficiency
            base_allocation = 30.0 + (normalized_score * 60.0)  # 30-90%
            
            # Adjust based on node type capacity
            type_factor = min(1.0, node.profile.cpu_capacity / 32.0)  # Normalize to max capacity
            
            final_allocation = base_allocation * type_factor
            final_allocation = np.clip(final_allocation, 10.0, 90.0)
            
            allocation[node_id] = {
                "cpu": float(final_allocation),
                "memory": float(final_allocation * 0.95)
            }
        
        # Offline nodes get zero allocation
        for node in nodes:
            if not node.is_available():
                allocation[node.node_id] = {"cpu": 0, "memory": 0}
        
        return allocation
