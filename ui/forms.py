"""
Forms Module
Input validation and data marshaling for simulation requests.

Responsibility: Validate user input, no execution logic.
"""

from typing import Dict, Any, List
from simulation.node_types import NodeType, get_node_type_by_name
from strategies import (
    StaticStrategy, CentralizedStrategy, 
    FederatedStrategy, EnergyAwareStrategy
)


class SimulationForm:
    """
    Represents a validated simulation request.
    
    Attributes:
        node_types: List of node types to simulate
        strategy_name: Which allocation strategy to use
        num_rounds: Number of federated rounds
        num_nodes_per_type: How many nodes of each type
        alpha, beta, gamma: Optimization weights (for federated strategy)
        sla_cpu, sla_memory: SLA thresholds
    """
    
    VALID_STRATEGIES = [
        "Static Allocation",
        "Centralized ML",
        "Federated Learning",
        "Energy-Aware Heuristic"
    ]
    
    def __init__(self):
        """Initialize empty form."""
        self.node_types: List[NodeType] = []
        self.strategy_name: str = "Federated Learning"
        self.num_rounds: int = 5
        self.num_nodes_per_type: int = 1
        self.alpha: float = 0.4
        self.beta: float = 0.35
        self.gamma: float = 0.25
        self.sla_cpu: float = 80.0
        self.sla_memory: float = 85.0
        self.errors: Dict[str, str] = {}
    
    @staticmethod
    def from_json(data: Dict[str, Any]) -> 'SimulationForm':
        """
        Create form from JSON request.
        
        Args:
            data: Dictionary from request.json
            
        Returns:
            SimulationForm instance with validated data
        """
        form = SimulationForm()
        
        # Parse node types
        node_type_names = data.get("node_types", [])
        if isinstance(node_type_names, str):
            node_type_names = [node_type_names]
        
        try:
            form.node_types = [get_node_type_by_name(nt) for nt in node_type_names]
            if not form.node_types:
                form.node_types = list(NodeType)  # Default: all types
        except ValueError as e:
            form.errors["node_types"] = str(e)
        
        # Parse strategy
        form.strategy_name = data.get("strategy", "Federated Learning")
        if form.strategy_name not in form.VALID_STRATEGIES:
            form.errors["strategy"] = f"Invalid strategy: {form.strategy_name}"
            form.strategy_name = "Federated Learning"
        
        # Parse parameters
        try:
            form.num_rounds = int(data.get("num_rounds", 5))
            if form.num_rounds < 1 or form.num_rounds > 100:
                form.errors["num_rounds"] = "Must be between 1 and 100"
                form.num_rounds = 5
        except (TypeError, ValueError):
            form.errors["num_rounds"] = "Must be an integer"
        
        try:
            form.num_nodes_per_type = int(data.get("num_nodes_per_type", 1))
            if form.num_nodes_per_type < 1 or form.num_nodes_per_type > 20:
                form.errors["num_nodes_per_type"] = "Must be between 1 and 20"
                form.num_nodes_per_type = 1
        except (TypeError, ValueError):
            form.errors["num_nodes_per_type"] = "Must be an integer"
        
        # Parse optimization weights
        try:
            form.alpha = float(data.get("alpha", 0.4))
            if not (0 <= form.alpha <= 1):
                form.errors["alpha"] = "Must be between 0 and 1"
                form.alpha = 0.4
        except (TypeError, ValueError):
            form.errors["alpha"] = "Must be a number"
        
        try:
            form.beta = float(data.get("beta", 0.35))
            if not (0 <= form.beta <= 1):
                form.errors["beta"] = "Must be between 0 and 1"
                form.beta = 0.35
        except (TypeError, ValueError):
            form.errors["beta"] = "Must be a number"
        
        try:
            form.gamma = float(data.get("gamma", 0.25))
            if not (0 <= form.gamma <= 1):
                form.errors["gamma"] = "Must be between 0 and 1"
                form.gamma = 0.25
        except (TypeError, ValueError):
            form.errors["gamma"] = "Must be a number"
        
        # Parse SLA thresholds
        try:
            form.sla_cpu = float(data.get("sla_cpu", 80.0))
            if not (50 <= form.sla_cpu <= 100):
                form.errors["sla_cpu"] = "Must be between 50 and 100"
                form.sla_cpu = 80.0
        except (TypeError, ValueError):
            form.errors["sla_cpu"] = "Must be a number"
        
        try:
            form.sla_memory = float(data.get("sla_memory", 85.0))
            if not (50 <= form.sla_memory <= 100):
                form.errors["sla_memory"] = "Must be between 50 and 100"
                form.sla_memory = 85.0
        except (TypeError, ValueError):
            form.errors["sla_memory"] = "Must be a number"
        
        return form
    
    def is_valid(self) -> bool:
        """Check if form has errors."""
        return len(self.errors) == 0
    
    def get_validation_errors(self) -> Dict[str, str]:
        """Get all validation errors."""
        return self.errors.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "node_types": [nt.value for nt in self.node_types],
            "strategy_name": self.strategy_name,
            "num_rounds": self.num_rounds,
            "num_nodes_per_type": self.num_nodes_per_type,
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma,
            "sla_cpu": self.sla_cpu,
            "sla_memory": self.sla_memory
        }
