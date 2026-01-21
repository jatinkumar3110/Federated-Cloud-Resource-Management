"""
Orchestration Layer: Execution Pipeline Module
Coordinates the entire federated learning workflow.

Responsibility: Orchestrate layer interactions without breaking SRP.
Called from: app.py only
"""

import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime

from simulation.workload import WorkloadGenerator
from simulation.resource_monitor import ResourceMonitor
from federated.model import FederatedNeuralNetwork
from federated.trainer import FederatedClient, FederatedServer
from metrics.evaluator import MetricsEvaluator


class FederatedLearningPipeline:
    """
    Orchestrates federated learning execution.
    
    Execution Flow:
    1. Generate workloads
    2. Monitor resources
    3. Federated training
    4. Evaluate metrics
    5. Log results
    """
    
    def __init__(self, num_clients: int = 3, random_seed: int = 42):
        """
        Initialize pipeline.
        
        Args:
            num_clients: Number of federated clients
            random_seed: Seed for reproducibility
        """
        np.random.seed(random_seed)
        
        self.num_clients = num_clients
        self.random_seed = random_seed
        
        # Initialize components
        self.workload_gen = WorkloadGenerator(intensity=0.6, random_seed=random_seed)
        self.resource_monitor = ResourceMonitor()
        self.global_model = FederatedNeuralNetwork(input_size=4, output_size=1, random_seed=random_seed)
        self.server = FederatedServer(self.global_model)
        self.evaluator = MetricsEvaluator()
        
        # Initialize clients
        self.clients = [
            FederatedClient(i, self.global_model) 
            for i in range(num_clients)
        ]
        
        self.execution_history: List[Dict] = []
    
    def generate_synthetic_data(self, num_samples: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic training data with NORMALIZED inputs.
        
        UPDATED (v2.0):
        - X features are normalized to [0,1]
        - y targets are optimization_scores, not raw metrics
        
        Args:
            num_samples: Number of data samples
            
        Returns:
            Tuple of (normalized_features, optimization_scores)
        """
        from config import OPTIMIZATION_CONFIG
        
        # Features: [cpu, memory, disk, workload] - RAW [0, 100]
        X_raw = np.random.rand(num_samples, 4) * 100
        
        # NORMALIZE features to [0, 1]
        X_normalized = X_raw / 100.0
        
        # Generate optimization_score targets
        # score = α*energy + β*imbalance + γ*sla_penalty
        alpha = OPTIMIZATION_CONFIG['alpha']
        beta = OPTIMIZATION_CONFIG['beta']
        gamma = OPTIMIZATION_CONFIG['gamma']
        
        y = np.zeros((num_samples, 1))
        for i in range(num_samples):
            cpu = X_raw[i, 0]
            mem = X_raw[i, 1]
            
            # Compute components
            energy = (cpu/100 * 0.6) + (mem/100 * 0.4)
            imbalance = abs(cpu - mem) / 100.0
            sla_penalty = 1.0 if (cpu > 80 or mem > 85) else 0.0
            
            score = alpha * energy + beta * imbalance + gamma * sla_penalty
            y[i, 0] = np.clip(score, 0.0, 1.0)
        
        return X_normalized, y
    
    def distribute_data_to_clients(self, X: np.ndarray, y: np.ndarray) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Distribute data to clients (non-IID simulation).
        
        Args:
            X: Feature matrix
            y: Target vector
            
        Returns:
            List of (X_client, y_client) tuples
        """
        n = len(X)
        samples_per_client = n // self.num_clients
        
        client_data = []
        for i in range(self.num_clients):
            start_idx = i * samples_per_client
            end_idx = (i + 1) * samples_per_client if i < self.num_clients - 1 else n
            
            X_client = X[start_idx:end_idx]
            y_client = y[start_idx:end_idx]
            client_data.append((X_client, y_client))
        
        return client_data
    
    def run_federated_round(self, client_data: List[Tuple[np.ndarray, np.ndarray]], 
                           learning_rate: float = 0.01, epochs: int = 1,
                           alpha: float = None, beta: float = None, gamma: float = None) -> Dict:
        """
        Execute one federated learning round.
        
        UPDATED (v2.0):
        - Passes optimization weights to trainer
        - Works with normalized inputs and optimization_score targets
        
        Args:
            client_data: List of client data tuples (normalized X, optimization_scores y)
            learning_rate: Learning rate for local training
            epochs: Local training epochs
            alpha: Weight for energy (if None, use config default)
            beta: Weight for imbalance (if None, use config default)
            gamma: Weight for SLA (if None, use config default)
            
        Returns:
            Dictionary with round results
        """
        from config import OPTIMIZATION_CONFIG
        
        if alpha is None:
            alpha = OPTIMIZATION_CONFIG['alpha']
        if beta is None:
            beta = OPTIMIZATION_CONFIG['beta']
        if gamma is None:
            gamma = OPTIMIZATION_CONFIG['gamma']
        
        round_start = datetime.now()
        
        # Local training
        client_updates = []
        client_metrics = []
        
        for client, (X_client, y_client) in zip(self.clients, client_data):
            # Train locally with optimization weights
            train_info = client.train_local(X_client, y_client, learning_rate, epochs,
                                           alpha=alpha, beta=beta, gamma=gamma)
            client_metrics.append(train_info)
            
            # Collect update
            update = client.get_model_update()
            client_updates.append(update)
        
        # Collect resources before aggregation
        resources_before = self.resource_monitor.collect_metrics()
        
        # Server aggregation
        aggregation_info = self.server.aggregate_models(client_updates)
        
        # Collect resources after aggregation
        resources_after = self.resource_monitor.collect_metrics()
        
        round_duration = (datetime.now() - round_start).total_seconds()
        
        # Compute round statistics
        round_results = {
            "round": aggregation_info["round"],
            "num_clients": self.num_clients,
            "client_losses": [m["final_loss"] for m in client_metrics],
            "avg_client_loss": float(np.mean([m["final_loss"] for m in client_metrics])),
            "cpu_usage": resources_after["cpu"],
            "memory_usage": resources_after["memory"],
            "disk_usage": resources_after["disk"],
            "duration_seconds": round_duration
        }
        
        self.execution_history.append(round_results)
        return round_results
    
    def run_simulation(self, num_rounds: int = 5, alpha: float = None, beta: float = None, 
                      gamma: float = None, sla_cpu: float = None, sla_memory: float = None) -> Dict:
        """
        Run complete federated learning simulation with optimization parameters.
        
        Args:
            num_rounds: Number of federated rounds
            alpha: Weight for energy efficiency [0, 1]
            beta: Weight for resource balance [0, 1]
            gamma: Weight for SLA compliance [0, 1]
            sla_cpu: CPU SLA threshold [50, 100]
            sla_memory: Memory SLA threshold [50, 100]
            
        Returns:
            Summary of simulation results including system metrics
        """
        from config import OPTIMIZATION_CONFIG
        
        # Use defaults if not provided
        if alpha is None:
            alpha = OPTIMIZATION_CONFIG['alpha']
        if beta is None:
            beta = OPTIMIZATION_CONFIG['beta']
        if gamma is None:
            gamma = OPTIMIZATION_CONFIG['gamma']
        if sla_cpu is None:
            sla_cpu = OPTIMIZATION_CONFIG['sla_cpu_threshold']
        if sla_memory is None:
            sla_memory = OPTIMIZATION_CONFIG['sla_memory_threshold']
        
        # Generate data
        X, y = self.generate_synthetic_data(num_samples=200)
        client_data = self.distribute_data_to_clients(X, y)
        
        # Run federated rounds
        round_results = []
        all_losses = []
        all_cpu = []
        all_memory = []
        
        for round_num in range(num_rounds):
            result = self.run_federated_round(client_data, learning_rate=0.01, epochs=2,
                                             alpha=alpha, beta=beta, gamma=gamma)
            round_results.append(result)
            all_losses.extend(result["client_losses"])
            all_cpu.append(result["cpu_usage"])
            all_memory.append(result["memory_usage"])
            
            # Log metrics
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "round": round_num + 1,
                "avg_loss": result["avg_client_loss"],
                "cpu": result["cpu_usage"],
                "memory": result["memory_usage"],
                "disk": result["disk_usage"]
            }
            self.evaluator.log_metrics_to_csv(log_entry)
        
        # Compute final metrics
        final_losses = [r["avg_client_loss"] for r in round_results]
        federated_metrics = self.evaluator.compute_federated_metrics(final_losses)
        
        # Compute system optimization metrics (v2.0)
        avg_cpu = float(np.mean(all_cpu)) if all_cpu else 0.0
        avg_memory = float(np.mean(all_memory)) if all_memory else 0.0
        
        system_metrics = {
            "energy_score": self.evaluator.compute_system_energy(avg_cpu, avg_memory),
            "sla_violations": max(0, int(sum(1 for cpu in all_cpu if cpu > sla_cpu) + 
                                         sum(1 for mem in all_memory if mem > sla_memory))),
            "efficiency_score": self.evaluator.compute_resource_efficiency(all_cpu, all_memory, [0.0] * len(all_cpu)),
            "stability_score": self.evaluator.compute_training_stability(all_losses) if all_losses else 0.0,
            "avg_optimization_score": float(np.mean(y)) if len(y) > 0 else 0.0,
            "violation_rate": len([1 for cpu in all_cpu if cpu > sla_cpu] + 
                                [1 for mem in all_memory if mem > sla_memory]) / (len(all_cpu) + len(all_memory)) if (all_cpu or all_memory) else 0.0
        }
        
        return {
            "num_rounds": num_rounds,
            "num_clients": self.num_clients,
            "final_metrics": federated_metrics,
            "round_results": round_results,
            "system_metrics": system_metrics,
            "optimization_params": {
                "alpha": alpha,
                "beta": beta,
                "gamma": gamma,
                "sla_cpu": sla_cpu,
                "sla_memory": sla_memory
            }
        }
    
    def get_current_model_state(self) -> Dict:
        """
        Get current global model state.
        
        Returns:
            Model state dictionary
        """
        return self.server.get_global_model().get_model_state()
    
    def get_execution_summary(self) -> Dict:
        """
        Get execution history summary.
        
        Returns:
            Summary statistics
        """
        if not self.execution_history:
            return {"status": "No execution history"}
        
        losses = [r["avg_client_loss"] for r in self.execution_history]
        cpus = [r["cpu_usage"] for r in self.execution_history]
        memories = [r["memory_usage"] for r in self.execution_history]
        
        return {
            "total_rounds": len(self.execution_history),
            "avg_loss": float(np.mean(losses)),
            "min_loss": float(np.min(losses)),
            "max_loss": float(np.max(losses)),
            "avg_cpu": float(np.mean(cpus)),
            "avg_memory": float(np.mean(memories))
        }
