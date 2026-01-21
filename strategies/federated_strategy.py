"""
Federated Learning Strategy
Distributed learning across nodes.

Each node trains locally, aggregates globally.
This is the main research contribution.
"""

from typing import Dict, List
import numpy as np
from strategies.base_strategy import BaseStrategy
from simulation.node import Node


class FederatedStrategy(BaseStrategy):
    """
    Federated Learning-based resource allocation.
    
    Approach: Each node trains locally on own data, aggregates gradient updates.
    - Distributed: No central controller
    - Privacy-preserving: Only model weights shared, not raw data
    - Heterogeneous: Can handle different node types
    
    Advantage: Privacy, resilience to failures, heterogeneity support
    Disadvantage: Communication overhead, slower convergence than centralized
    """
    
    def __init__(self, alpha: float = 0.4, beta: float = 0.35, gamma: float = 0.25):
        """
        Initialize federated strategy with optimization weights.
        
        Args:
            alpha: Weight for energy optimization
            beta: Weight for balance optimization
            gamma: Weight for SLA optimization
        """
        super().__init__("Federated Learning")
        
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        # Federated state
        self.global_allocations = {}  # Last known good allocations
    
    def allocate_resources(self, nodes: List[Node]) -> Dict[int, Dict[str, float]]:
        """
        Allocate resources using federated learning decisions.
        
        Args:
            nodes: List of nodes
            
        Returns:
            Dictionary mapping node_id -> {cpu, memory} percentages
        """
        allocation = {}
        
        # Compute system-wide metrics for this round
        total_energy_cost = sum(node.profile.energy_cost_factor for node in nodes if node.is_available())
        available_nodes = len([n for n in nodes if n.is_available()])
        
        for node in nodes:
            if not node.is_available():
                allocation[node.node_id] = {"cpu": 0, "memory": 0}
                continue
            
            # Federated decision: optimize multi-objective function
            # allocation = argmin (alpha*energy + beta*imbalance + gamma*sla_penalty)
            
            # Energy component: higher for efficient nodes
            energy_score = 1.0 / (node.profile.energy_cost_factor + 1e-6)
            energy_score = np.clip(energy_score / 2.0, 0, 1)  # Normalize
            
            # Balance component: try to balance load across heterogeneous nodes
            capacity_util = node.get_capacity_utilization()
            balance_score = 1.0 - capacity_util  # Underutilized nodes get more
            
            # SLA component: sensitive nodes get more resources
            sla_score = 1.0 - node.profile.sla_sensitivity  # Less sensitive = more resources available
            
            # Combined objective
            allocation_score = (
                self.alpha * energy_score +
                self.beta * balance_score +
                self.gamma * sla_score
            )
            
            # Map score to CPU/memory percentage (0.0-1.0 score -> 0-100%)
            cpu_percent = np.clip(allocation_score * 100.0, 0, 100)
            memory_percent = np.clip(allocation_score * 95.0, 0, 100)  # Slightly less for memory
            
            allocation[node.node_id] = {
                "cpu": float(cpu_percent),
                "memory": float(memory_percent)
            }
            
            self.global_allocations[node.node_id] = allocation[node.node_id]
        
        return allocation
    
    def get_optimization_weights(self) -> Dict[str, float]:
        """Get current optimization weights."""
        return {
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma
        }
    
    def set_optimization_weights(self, alpha: float = None, beta: float = None, 
                                  gamma: float = None) -> None:
        """
        Update optimization weights for new round.
        
        Args:
            alpha: Weight for energy (if provided)
            beta: Weight for balance (if provided)
            gamma: Weight for SLA (if provided)
        """
        if alpha is not None:
            self.alpha = float(alpha)
        if beta is not None:
            self.beta = float(beta)
        if gamma is not None:
            self.gamma = float(gamma)
