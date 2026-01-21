"""
Federated Learning Layer: Model Definition Module
Defines neural network model for federated learning.

Responsibility: Model architecture and inference only (no training).
UPDATED (v2.0): Now outputs policy values that minimize optimization_score
"""

import numpy as np
from typing import Tuple
from copy import deepcopy


class FederatedNeuralNetwork:
    """
    Simple feedforward neural network for federated learning.
    
    UPDATED: Now predicts optimal allocation policy (not raw metrics).
    - Input: Normalized resource metrics [cpu, memory, disk, workload] ∈ [0,1]
    - Output: Policy value ∈ [0,1] representing allocation decision
    - Target: Minimize optimization_score (energy + imbalance + SLA_penalty)
    
    Attributes:
        input_size (int): Input feature dimension
        output_size (int): Output dimension (policy value)
        weights (np.ndarray): Model weights [input_size, output_size]
        bias (np.ndarray): Bias term [1, output_size]
    """
    
    def __init__(self, input_size: int = 4, output_size: int = 1, random_seed: int = 42):
        """
        Initialize federated model.
        
        Args:
            input_size: Dimension of input features (4: cpu, mem, disk, workload)
            output_size: Dimension of output (1: policy value in [0,1])
            random_seed: Seed for reproducibility
        """
        np.random.seed(random_seed)
        self.input_size = input_size
        self.output_size = output_size
        
        # Xavier initialization for numerical stability
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(1.0 / input_size)
        self.bias = np.zeros((1, output_size))
    
    def forward(self, X: np.ndarray) -> np.ndarray:
        """
        Forward pass (inference).
        
        UPDATED: Output is clipped to [0,1] as policy value.
        
        Args:
            X: Input features [batch_size, input_size] - NORMALIZED to [0,1]
            
        Returns:
            Policy values [batch_size, output_size] ∈ [0,1]
        """
        if X.ndim == 1:
            X = X.reshape(1, -1)
        output = np.dot(X, self.weights) + self.bias
        # Clip to [0, 1] to represent valid policy values
        return np.clip(output, 0.0, 1.0)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            X: Input features (normalized to [0,1])
            
        Returns:
            Predicted policy values in [0,1]
        """
        return self.forward(X)
    
    def get_weights(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get current model parameters.
        
        Returns:
            Tuple of (weights, bias)
        """
        return (deepcopy(self.weights), deepcopy(self.bias))
    
    def set_weights(self, weights: np.ndarray, bias: np.ndarray) -> None:
        """
        Set model parameters.
        
        Args:
            weights: Weight matrix to set
            bias: Bias vector to set
        """
        self.weights = deepcopy(weights)
        self.bias = deepcopy(bias)
    
    def get_model_state(self) -> dict:
        """
        Serialize model state for aggregation.
        
        Returns:
            Dictionary containing model parameters
        """
        return {
            "weights": deepcopy(self.weights),
            "bias": deepcopy(self.bias),
            "input_size": self.input_size,
            "output_size": self.output_size
        }
