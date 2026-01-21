"""
Dashboard Controller
Orchestrates dashboard interactions and simulation setup.

Responsibility: Manage simulation lifecycle, no execution.
"""

from typing import Dict, List, Any
from ui.forms import SimulationForm
from simulation.node import Node
from simulation.node_types import NodeType
from strategies import (
    BaseStrategy, StaticStrategy, CentralizedStrategy,
    FederatedStrategy, EnergyAwareStrategy
)


class DashboardController:
    """
    Controls dashboard interactions and simulation setup.
    
    Responsibility: Translate UI inputs to executable configuration.
    """
    
    @staticmethod
    def get_available_node_types() -> List[Dict[str, Any]]:
        """
        Get list of available node types for UI selection.
        
        Returns:
            List of {name, value, description} dicts
        """
        descriptions = {
            "edge_device": "IoT/edge servers (2 CPU, 4GB RAM)",
            "user_device": "Mobile/laptops (4 CPU, 8GB RAM)",
            "compute_server": "On-premises servers (16 CPU, 32GB RAM)",
            "data_center_node": "Cloud datacenter (32 CPU, 64GB RAM)"
        }
        
        return [
            {
                "name": nt.value,
                "value": nt.value,
                "description": descriptions.get(nt.value, "")
            }
            for nt in NodeType
        ]
    
    @staticmethod
    def get_available_strategies() -> List[Dict[str, str]]:
        """
        Get list of available strategies for UI selection.
        
        Returns:
            List of {name, value, description} dicts
        """
        strategies = [
            {
                "name": "Static Allocation",
                "value": "Static Allocation",
                "description": "Fixed rules based on node type"
            },
            {
                "name": "Centralized ML",
                "value": "Centralized ML",
                "description": "Central controller with ML model"
            },
            {
                "name": "Federated Learning",
                "value": "Federated Learning",
                "description": "Distributed learning across nodes (main research)"
            },
            {
                "name": "Energy-Aware Heuristic",
                "value": "Energy-Aware Heuristic",
                "description": "Simple energy-efficiency rules"
            }
        ]
        return strategies
    
    @staticmethod
    def create_strategy(strategy_name: str, **kwargs) -> BaseStrategy:
        """
        Create strategy instance from name.
        
        Args:
            strategy_name: Name of strategy
            **kwargs: Additional parameters (alpha, beta, gamma for federated)
            
        Returns:
            Strategy instance
            
        Raises:
            ValueError: If strategy name invalid
        """
        strategy_map = {
            "Static Allocation": StaticStrategy,
            "Centralized ML": CentralizedStrategy,
            "Federated Learning": FederatedStrategy,
            "Energy-Aware Heuristic": EnergyAwareStrategy
        }
        
        if strategy_name not in strategy_map:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy_class = strategy_map[strategy_name]
        
        # Pass kwargs only if strategy accepts them
        if strategy_name == "Federated Learning":
            return strategy_class(
                alpha=kwargs.get("alpha", 0.4),
                beta=kwargs.get("beta", 0.35),
                gamma=kwargs.get("gamma", 0.25)
            )
        else:
            return strategy_class()
    
    @staticmethod
    def create_nodes(node_types: List[NodeType], num_per_type: int) -> List[Node]:
        """
        Create nodes from specifications.
        
        Args:
            node_types: List of node types
            num_per_type: Number of nodes per type
            
        Returns:
            List of created Node objects
        """
        nodes = []
        node_id = 0
        
        for node_type in node_types:
            for _ in range(num_per_type):
                node = Node(node_id=node_id, node_type=node_type)
                nodes.append(node)
                node_id += 1
        
        return nodes
    
    @staticmethod
    def validate_request(data: Dict[str, Any]) -> tuple[bool, SimulationForm]:
        """
        Validate simulation request.
        
        Args:
            data: Request data
            
        Returns:
            Tuple of (is_valid, form)
        """
        form = SimulationForm.from_json(data)
        return form.is_valid(), form
    
    @staticmethod
    def get_dashboard_metadata() -> Dict[str, Any]:
        """
        Get metadata for dashboard UI initialization.
        
        Returns:
            Dictionary with node types, strategies, defaults
        """
        return {
            "node_types": DashboardController.get_available_node_types(),
            "strategies": DashboardController.get_available_strategies(),
            "defaults": {
                "node_types": ["edge_device", "user_device", "compute_server"],
                "strategy": "Federated Learning",
                "num_rounds": 5,
                "num_nodes_per_type": 2,
                "alpha": 0.4,
                "beta": 0.35,
                "gamma": 0.25,
                "sla_cpu": 80.0,
                "sla_memory": 85.0
            }
        }
