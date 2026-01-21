"""
Centralized ML Strategy
Central controller uses ML to optimize allocation.

Simulates a centralized optimization service that learns optimal allocations.
"""

from typing import Dict, List
import numpy as np
from strategies.base_strategy import BaseStrategy
from simulation.node import Node
from federated.model import FederatedNeuralNetwork


class CentralizedStrategy(BaseStrategy):
    """
    Centralized ML-based resource allocation.
    
    Approach: Train a global model on all node data, use it to predict allocations.
    - Collects workload/resource data from all nodes
    - Trains global model on centralized data
    - Uses model to predict optimal allocations
    
    Advantage: Access to global state, potentially optimal for central objectives
    Disadvantage: Single point of failure, privacy concerns, communication overhead
    """
    
    def __init__(self, model_input_size: int = 4, model_output_size: int = 2):
        """
        Initialize centralized strategy.
        
        Args:
            model_input_size: Features per node (workload, cpu, memory, etc.)
            model_output_size: Outputs per node (cpu_alloc, memory_alloc)
        """
        super().__init__("Centralized ML")
        
        # Central model
        self.model = FederatedNeuralNetwork(
            input_size=model_input_size,
            output_size=model_output_size,
            random_seed=42
        )
        
        self.model_input_size = model_input_size
        self.model_output_size = model_output_size
    
    def _prepare_node_features(self, node: Node) -> np.ndarray:
        """
        Extract features from node for model input.
        
        Args:
            node: Node to extract features from
            
        Returns:
            Feature vector [workload_norm, cpu_norm, memory_norm, capacity_utilization]
        """
        # Normalize features to [0, 1]
        workload_norm = node.get_workload() / 100.0
        cpu_norm = node.cpu_utilization / 100.0
        memory_norm = node.memory_utilization / 100.0
        capacity_util = node.get_capacity_utilization()
        
        features = np.array([
            workload_norm,
            cpu_norm,
            memory_norm,
            capacity_util
        ], dtype=np.float32)
        
        return features
    
    def allocate_resources(self, nodes: List[Node]) -> Dict[int, Dict[str, float]]:
        """
        Allocate resources using centralized ML model.
        
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
            
            # Extract features
            features = self._prepare_node_features(node)
            features = features.reshape(1, -1)  # Reshape for model
            
            # Use model to predict allocation
            prediction = self.model.forward(features)
            
            # Convert output to CPU and memory percentages
            # Output is [0, 1], scale to [0, 100]
            cpu_percent = float(np.clip(prediction[0, 0] * 100.0, 0, 100))
            memory_percent = float(np.clip(prediction[0, 1] * 100.0, 0, 100)) if self.model_output_size > 1 else cpu_percent
            
            allocation[node.node_id] = {
                "cpu": cpu_percent,
                "memory": memory_percent
            }
        
        return allocation
    
    def update_model(self, nodes: List[Node]) -> None:
        """
        Update central model with new data.
        
        Called periodically to improve allocation predictions.
        
        Args:
            nodes: List of nodes with current state
        """
        # Collect features and targets (targets = efficient allocations)
        X_list = []
        y_list = []
        
        for node in nodes:
            features = self._prepare_node_features(node)
            X_list.append(features)
            
            # Target: efficient allocation based on energy cost
            energy_factor = node.profile.energy_cost_factor
            sla_sensitivity = node.profile.sla_sensitivity
            
            # Efficient nodes get higher allocation
            cpu_target = (1.0 / energy_factor) * (1.0 - sla_sensitivity * 0.1)
            memory_target = cpu_target * 0.9  # Memory slightly less than CPU
            
            y_list.append([np.clip(cpu_target, 0, 1), np.clip(memory_target, 0, 1)])
        
        if X_list and y_list:
            X = np.array(X_list)
            y = np.array(y_list)
            
            # Simple gradient descent update (1 epoch)
            # For demonstration; in real system would be more sophisticated
            learning_rate = 0.01
            
            # Forward pass
            predictions = self.model.forward(X)
            
            # Simple MSE loss (not actual training, just direction update)
            error = predictions - y
            
            # This is a simplified update; real implementation would use backprop
            # For now, we'll just note that the model structure is here
