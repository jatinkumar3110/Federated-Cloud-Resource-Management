"""
Scenario Manager Module
Defines experiment scenarios for batch runs.

Responsibility: Scenario specification, parameter variation, result storage.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import json


@dataclass
class Scenario:
    """Single experiment scenario specification."""
    
    name: str
    description: str
    num_rounds: int
    num_nodes_per_type: Dict[str, int]
    strategies: List[str]
    alpha: float = 0.4
    beta: float = 0.35
    gamma: float = 0.25
    sla_cpu: float = 80.0
    sla_memory: float = 80.0
    custom_nodes: Optional[List[Any]] = field(default=None)  # List of Node objects for custom scenarios
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scenario to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "num_rounds": self.num_rounds,
            "num_nodes_per_type": self.num_nodes_per_type,
            "strategies": self.strategies,
            "alpha": self.alpha,
            "beta": self.beta,
            "gamma": self.gamma,
            "sla_cpu": self.sla_cpu,
            "sla_memory": self.sla_memory,
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Scenario":
        """Create scenario from dictionary."""
        return Scenario(
            name=data.get("name", "Unnamed"),
            description=data.get("description", ""),
            num_rounds=data.get("num_rounds", 5),
            num_nodes_per_type=data.get("num_nodes_per_type", 
                                       {"edge_device": 1, "user_device": 1}),
            strategies=data.get("strategies", ["static"]),
            alpha=data.get("alpha", 0.4),
            beta=data.get("beta", 0.35),
            gamma=data.get("gamma", 0.25),
            sla_cpu=data.get("sla_cpu", 80.0),
            sla_memory=data.get("sla_memory", 80.0),
        )


class ScenarioManager:
    """
    Manages experiment scenarios and predefined settings.
    
    Provides:
    - Standard benchmark scenarios
    - Custom scenario creation
    - Scenario persistence (JSON)
    - Scenario variation/sweeps
    """
    
    # Predefined standard scenarios
    STANDARD_SCENARIOS = {
        "small_scale": Scenario(
            name="Small Scale",
            description="Small heterogeneous deployment (3 nodes, 5 rounds)",
            num_rounds=5,
            num_nodes_per_type={
                "edge_device": 1,
                "user_device": 1,
                "compute_server": 1,
            },
            strategies=["Static Allocation", "Centralized ML", "Federated Learning", "Energy-Aware Heuristic"],
        ),
        "medium_scale": Scenario(
            name="Medium Scale",
            description="Medium deployment (8 nodes, 10 rounds)",
            num_rounds=10,
            num_nodes_per_type={
                "edge_device": 2,
                "user_device": 2,
                "compute_server": 2,
                "data_center_node": 2,
            },
            strategies=["Static Allocation", "Centralized ML", "Federated Learning", "Energy-Aware Heuristic"],
        ),
        "large_scale": Scenario(
            name="Large Scale",
            description="Large deployment (20 nodes, 20 rounds)",
            num_rounds=20,
            num_nodes_per_type={
                "edge_device": 5,
                "user_device": 5,
                "compute_server": 5,
                "data_center_node": 5,
            },
            strategies=["Static Allocation", "Centralized ML", "Federated Learning", "Energy-Aware Heuristic"],
        ),
        "edge_heavy": Scenario(
            name="Edge-Heavy",
            description="Edge-dominated deployment (10 edge, 2 datacenter)",
            num_rounds=15,
            num_nodes_per_type={
                "edge_device": 10,
                "user_device": 0,
                "compute_server": 0,
                "data_center_node": 2,
            },
            strategies=["Static Allocation", "Federated Learning", "Energy-Aware Heuristic"],
        ),
        "cloud_heavy": Scenario(
            name="Cloud-Heavy",
            description="Cloud-dominated deployment (2 edge, 10 datacenter)",
            num_rounds=15,
            num_nodes_per_type={
                "edge_device": 2,
                "user_device": 0,
                "compute_server": 0,
                "data_center_node": 10,
            },
            strategies=["Static Allocation", "Centralized ML", "Federated Learning"],
        ),
        "balanced": Scenario(
            name="Balanced",
            description="Balanced heterogeneous deployment",
            num_rounds=10,
            num_nodes_per_type={
                "edge_device": 4,
                "user_device": 4,
                "compute_server": 4,
                "data_center_node": 4,
            },
            strategies=["Static Allocation", "Centralized ML", "Federated Learning", "Energy-Aware Heuristic"],
        ),
    }
    
    @staticmethod
    def get_standard_scenario(name: str) -> Scenario:
        """
        Get a standard scenario by name.
        
        Args:
            name: Scenario name (e.g., "small_scale", "medium_scale")
            
        Returns:
            Scenario object
        """
        if name not in ScenarioManager.STANDARD_SCENARIOS:
            raise ValueError(f"Unknown scenario: {name}")
        
        return ScenarioManager.STANDARD_SCENARIOS[name]
    
    @staticmethod
    def list_standard_scenarios() -> List[str]:
        """Get list of available standard scenarios."""
        return list(ScenarioManager.STANDARD_SCENARIOS.keys())
    
    @staticmethod
    def describe_scenario(name: str) -> str:
        """Get description of scenario."""
        scenario = ScenarioManager.get_standard_scenario(name)
        return scenario.description
    
    @staticmethod
    def create_custom_scenario(
        name: str,
        description: str,
        num_rounds: int,
        num_nodes_per_type: Dict[str, int],
        strategies: List[str],
        alpha: float = 0.4,
        beta: float = 0.35,
        gamma: float = 0.25,
        sla_cpu: float = 80.0,
        sla_memory: float = 80.0,
    ) -> Scenario:
        """
        Create a custom experiment scenario.
        
        Args:
            name: Scenario name
            description: Human-readable description
            num_rounds: Number of federated rounds
            num_nodes_per_type: Dict with node type counts
            strategies: List of strategies to compare
            alpha: Weight for energy in federated strategy
            beta: Weight for balance
            gamma: Weight for SLA
            sla_cpu: CPU SLA threshold
            sla_memory: Memory SLA threshold
            
        Returns:
            New Scenario object
        """
        return Scenario(
            name=name,
            description=description,
            num_rounds=num_rounds,
            num_nodes_per_type=num_nodes_per_type,
            strategies=strategies,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            sla_cpu=sla_cpu,
            sla_memory=sla_memory,
        )
    
    @staticmethod
    def save_scenario(scenario: Scenario, filepath: str):
        """
        Save scenario to JSON file.
        
        Args:
            scenario: Scenario to save
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            json.dump(scenario.to_dict(), f, indent=2)
        print(f"Scenario saved: {filepath}")
    
    @staticmethod
    def load_scenario(filepath: str) -> Scenario:
        """
        Load scenario from JSON file.
        
        Args:
            filepath: Input file path
            
        Returns:
            Loaded Scenario object
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        return Scenario.from_dict(data)
    
    @staticmethod
    def create_parameter_sweep(
        base_scenario: Scenario,
        param_name: str,
        param_values: List[Any],
    ) -> List[Scenario]:
        """
        Create scenario variants by sweeping a parameter.
        
        Args:
            base_scenario: Base scenario to vary
            param_name: Parameter to sweep (e.g., "alpha", "num_rounds")
            param_values: List of values to try
            
        Returns:
            List of scenario variants
        """
        scenarios = []
        
        for value in param_values:
            variant_dict = base_scenario.to_dict()
            
            # Update the parameter
            if param_name in variant_dict:
                variant_dict[param_name] = value
                variant_dict["name"] = f"{base_scenario.name} ({param_name}={value})"
            else:
                continue
            
            scenarios.append(Scenario.from_dict(variant_dict))
        
        return scenarios
    
    @staticmethod
    def create_strategy_sweep(
        base_scenario: Scenario,
        strategies_to_test: List[str],
    ) -> List[Scenario]:
        """
        Create scenario variants testing different strategies.
        
        Args:
            base_scenario: Base scenario
            strategies_to_test: Strategies to include
            
        Returns:
            List of scenario variants
        """
        return ScenarioManager.create_parameter_sweep(
            base_scenario,
            "strategies",
            [strategies_to_test]
        )
    
    @staticmethod
    def create_scale_sweep(
        node_counts: List[int],
    ) -> List[Scenario]:
        """
        Create scenarios with increasing scale.
        
        Args:
            node_counts: List of total node counts to test
            
        Returns:
            List of scaled scenario variants
        """
        scenarios = []
        
        for count in node_counts:
            # Distribute nodes across types proportionally
            per_type = count // 4
            remainder = count % 4
            
            num_nodes_per_type = {
                "edge_device": per_type + (1 if remainder >= 1 else 0),
                "user_device": per_type + (1 if remainder >= 2 else 0),
                "compute_server": per_type + (1 if remainder >= 3 else 0),
                "data_center_node": per_type,
            }
            
            scenario = Scenario(
                name=f"Scale-{count}",
                description=f"Experiment with {count} total nodes",
                num_rounds=10,
                num_nodes_per_type=num_nodes_per_type,
                strategies=["static", "centralized", "federated", "energy_aware"],
            )
            scenarios.append(scenario)
        
        return scenarios
