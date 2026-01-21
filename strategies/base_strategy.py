"""
Base Strategy Class
Abstract base for all resource allocation strategies.

All strategies must:
- Implement allocate_resources(nodes) -> allocation_dict
- Be composable with different node types
- Track metrics internally
- Be comparable using same metrics

Responsibility: Define strategy interface and common utilities.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from simulation.node import Node


class BaseStrategy(ABC):
    """
    Abstract base class for resource allocation strategies.
    
    Each strategy represents a different approach to cloud resource management:
    - Static: Fixed allocation rules
    - Centralized: ML-based central controller
    - Federated: Distributed FL-based optimization
    - Energy-aware: Heuristics prioritizing efficiency
    """
    
    def __init__(self, strategy_name: str):
        """
        Initialize strategy.
        
        Args:
            strategy_name: Human-readable name for this strategy
        """
        self.strategy_name = strategy_name
        self.allocation_history: List[Dict[str, Any]] = []
        self.total_energy = 0.0
        self.total_sla_violations = 0
        self.rounds_executed = 0
    
    @abstractmethod
    def allocate_resources(self, nodes: List[Node]) -> Dict[int, Dict[str, float]]:
        """
        Allocate resources to nodes based on strategy logic.
        
        MUST be implemented by subclasses.
        
        Args:
            nodes: List of Node objects to allocate resources to
            
        Returns:
            Dictionary mapping node_id -> {cpu_percent, memory_percent}
        """
        pass
    
    def execute_allocation(self, nodes: List[Node]) -> Dict[int, Dict[str, float]]:
        """
        Execute allocation and track metrics.
        
        Wrapper around allocate_resources that handles logging.
        
        Args:
            nodes: List of nodes
            
        Returns:
            Allocation dictionary
        """
        allocation = self.allocate_resources(nodes)
        
        # Track round
        self.rounds_executed += 1
        
        # Apply allocation to nodes and track metrics
        round_metrics = {
            "round": self.rounds_executed,
            "strategy": self.strategy_name,
            "allocations": allocation,
            "node_states": {}
        }
        
        for node_id, alloc in allocation.items():
            # Find node with this ID
            node = next((n for n in nodes if n.node_id == node_id), None)
            if node is not None:
                # Apply allocation
                node.allocate_resources(
                    cpu_percent=alloc.get("cpu", 0),
                    memory_percent=alloc.get("memory", 0)
                )
                
                # Track energy and SLA
                energy = node.compute_energy_consumption(duration_seconds=1.0)
                self.total_energy += energy
                
                if node.check_sla_violation():
                    self.total_sla_violations += 1
                
                # Store node state
                round_metrics["node_states"][node_id] = node.get_node_state()
        
        self.allocation_history.append(round_metrics)
        return allocation
    
    def get_strategy_name(self) -> str:
        """Get human-readable strategy name."""
        return self.strategy_name
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get cumulative strategy metrics.
        
        Returns:
            Dictionary with energy, SLA, convergence metrics
        """
        avg_energy = self.total_energy / max(self.rounds_executed, 1)
        sla_violation_rate = self.total_sla_violations / max(self.rounds_executed, 1)
        
        return {
            "strategy": self.strategy_name,
            "rounds_executed": self.rounds_executed,
            "total_energy": float(self.total_energy),
            "average_energy": float(avg_energy),
            "total_sla_violations": self.total_sla_violations,
            "sla_violation_rate": float(sla_violation_rate)
        }
    
    def get_allocation_history(self) -> List[Dict[str, Any]]:
        """Get complete allocation history."""
        return self.allocation_history.copy()
    
    def reset_metrics(self) -> None:
        """Reset strategy metrics (for new experiment)."""
        self.allocation_history = []
        self.total_energy = 0.0
        self.total_sla_violations = 0
        self.rounds_executed = 0
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Strategy({self.strategy_name})"
