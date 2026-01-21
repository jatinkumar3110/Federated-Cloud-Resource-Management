"""
Federated Learning Layer: Training Module
Implements federated learning algorithms with privacy considerations.

Responsibility: Model training and client-side updates only.
UPDATED (v2.0): Uses optimization_score as loss function (not MSE on raw metrics)
"""

import numpy as np
from typing import List, Dict, Tuple
from federated.model import FederatedNeuralNetwork
from simulation.workload import WorkloadGenerator
from copy import deepcopy


class FederatedClient:
    """
    Federated learning client for local training.
    
    UPDATED: Trains to minimize optimization_score (energy + imbalance + SLA)
    instead of predicting raw metrics.
    
    Simulates a distributed client that:
    1. Receives global model
    2. Trains on local data (normalized inputs)
    3. Sends updates to server
    """
    
    def __init__(self, client_id: int, model: FederatedNeuralNetwork):
        """
        Initialize federated client.
        
        Args:
            client_id: Unique client identifier
            model: Initial model instance
        """
        self.client_id = client_id
        self.model = deepcopy(model)
        self.local_loss = []
    
    def train_local(self, X: np.ndarray, y: np.ndarray, 
                   learning_rate: float = 0.01, epochs: int = 1,
                   alpha: float = 0.4, beta: float = 0.35, gamma: float = 0.25) -> Dict:
        """
        Train model on local data using optimization_score as target.
        
        UPDATED: y is now the optimization_score, not raw metrics.
        X is normalized to [0,1].
        
        Args:
            X: Local training features [n_samples, input_size] - NORMALIZED
            y: Optimization scores [n_samples, 1] representing target policy
            learning_rate: Learning rate for gradient descent
            epochs: Number of local epochs
            alpha: Weight for energy in loss (unused in this version, for compatibility)
            beta: Weight for imbalance (unused)
            gamma: Weight for SLA (unused)
            
        Returns:
            Dictionary with training metrics
        """
        initial_loss = self._compute_loss(X, y)
        
        for epoch in range(epochs):
            # Forward pass
            predictions = self.model.forward(X)
            loss = self._compute_loss(X, y)
            self.local_loss.append(loss)
            
            # Backward pass: compute gradients
            batch_size = X.shape[0]
            error = predictions - y
            
            grad_weights = np.dot(X.T, error) / batch_size
            grad_bias = np.mean(error, axis=0, keepdims=True)
            
            # Update weights
            weights, bias = self.model.get_weights()
            new_weights = weights - learning_rate * grad_weights
            new_bias = bias - learning_rate * grad_bias
            self.model.set_weights(new_weights, new_bias)
        
        final_loss = self._compute_loss(X, y)
        loss_improvement = initial_loss - final_loss
        
        return {
            "client_id": self.client_id,
            "initial_loss": float(initial_loss),
            "final_loss": float(final_loss),
            "loss_improvement": float(loss_improvement),
            "epochs": epochs
        }
    
    def _compute_loss(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Compute Mean Squared Error loss.
        
        Args:
            X: Input features
            y: Target values
            
        Returns:
            MSE loss value
        """
        predictions = self.model.forward(X)
        mse = np.mean((predictions - y) ** 2)
        return float(mse)
    
    def get_model_update(self) -> Dict:
        """
        Get model update for server aggregation.
        
        Returns:
            Model state dictionary
        """
        return self.model.get_model_state()


class FederatedServer:
    """
    Federated learning server for model aggregation.
    
    Implements FedAvg (Federated Averaging) algorithm.
    """
    
    def __init__(self, global_model: FederatedNeuralNetwork):
        """
        Initialize federated server.
        
        Args:
            global_model: Global model instance
        """
        self.global_model = deepcopy(global_model)
        self.aggregation_history: List[Dict] = []
    
    def aggregate_models(self, client_updates: List[Dict]) -> Dict:
        """
        Aggregate client model updates using FedAvg.
        
        Args:
            client_updates: List of model states from clients
            
        Returns:
            Dictionary with aggregation metrics
        """
        if not client_updates:
            raise ValueError("No client updates provided")
        
        num_clients = len(client_updates)
        
        # Average weights
        avg_weights = np.zeros_like(client_updates[0]["weights"])
        avg_bias = np.zeros_like(client_updates[0]["bias"])
        
        for update in client_updates:
            avg_weights += update["weights"] / num_clients
            avg_bias += update["bias"] / num_clients
        
        # Update global model
        self.global_model.set_weights(avg_weights, avg_bias)
        
        aggregation_info = {
            "round": len(self.aggregation_history) + 1,
            "num_clients": num_clients,
            "timestamp": str(np.datetime64('now'))
        }
        self.aggregation_history.append(aggregation_info)
        
        return aggregation_info
    
    def get_global_model(self) -> FederatedNeuralNetwork:
        """
        Get current global model for distribution.
        
        Returns:
            Copy of global model
        """
        return deepcopy(self.global_model)
