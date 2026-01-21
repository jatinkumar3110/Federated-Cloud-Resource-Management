"""
Communication Metrics Module
Measures communication overhead of distributed resource management.

Research question: What is the communication cost of federated learning
compared to centralized approaches?

Responsibility: Track and analyze communication patterns.
"""

from typing import List, Dict, Any
import numpy as np
from simulation.node import Node


class CommunicationMetrics:
    """
    Tracks and analyzes communication overhead in federated systems.
    
    Communication patterns:
    - Per-round overhead: Bytes per federated round
    - Total overhead: Cumulative bytes across all rounds
    - Bandwidth utilization: Bytes per second
    - Node contribution: Communication asymmetry
    """
    
    @staticmethod
    def compute_per_round_overhead(nodes: List[Node], num_rounds: int, 
                                   model_size_bytes: int = 512) -> float:
        """
        Compute total communication bytes per round.
        
        Args:
            nodes: List of participating nodes
            num_rounds: Number of federated rounds
            model_size_bytes: Size of model in bytes
            
        Returns:
            float: Bytes communicated per round
        """
        total_bytes_per_round = 0.0
        
        for node in nodes:
            if node.is_available():
                # Each node uploads model and downloads aggregated model
                upload_bytes = node.get_communication_cost(model_size_bytes)
                download_bytes = model_size_bytes  # Aggregated model
                
                total_bytes_per_round += upload_bytes + download_bytes
        
        return float(total_bytes_per_round)
    
    @staticmethod
    def compute_total_overhead(nodes: List[Node], num_rounds: int,
                              model_size_bytes: int = 512) -> float:
        """
        Compute total communication bytes across all rounds.
        
        Args:
            nodes: List of nodes
            num_rounds: Number of federated rounds
            model_size_bytes: Size of model in bytes
            
        Returns:
            float: Total bytes communicated
        """
        per_round = CommunicationMetrics.compute_per_round_overhead(
            nodes, num_rounds, model_size_bytes
        )
        return float(per_round * num_rounds)
    
    @staticmethod
    def compute_per_node_overhead(node: Node, num_rounds: int,
                                 model_size_bytes: int = 512) -> float:
        """
        Compute communication bytes for single node.
        
        Args:
            node: Node to analyze
            num_rounds: Number of rounds
            model_size_bytes: Model size
            
        Returns:
            float: Bytes for this node
        """
        if not node.is_available():
            return 0.0
        
        upload_per_round = node.get_communication_cost(model_size_bytes)
        download_per_round = model_size_bytes
        
        total = (upload_per_round + download_per_round) * num_rounds
        return float(total)
    
    @staticmethod
    def compute_communication_fairness(nodes: List[Node], num_rounds: int,
                                      model_size_bytes: int = 512) -> float:
        """
        Compute fairness of communication load across nodes.
        
        Some nodes (data center) may dominate communication.
        
        Args:
            nodes: List of nodes
            num_rounds: Number of rounds
            model_size_bytes: Model size
            
        Returns:
            float: Communication fairness in [0, 1]
        """
        overhead_per_node = [
            CommunicationMetrics.compute_per_node_overhead(
                n, num_rounds, model_size_bytes
            )
            for n in nodes if n.is_available()
        ]
        
        if len(overhead_per_node) == 0:
            return 1.0
        
        # Compute coefficient of variation
        overhead_array = np.array(overhead_per_node)
        mean = np.mean(overhead_array)
        
        if mean == 0:
            return 1.0
        
        std = np.std(overhead_array)
        cv = std / mean
        
        # Convert CV to fairness score (lower CV = higher fairness)
        fairness = 1.0 / (1.0 + cv)
        return float(fairness)
    
    @staticmethod
    def compute_bandwidth_per_node(node: Node, duration_seconds: float,
                                  model_size_bytes: int = 512) -> float:
        """
        Estimate bandwidth utilization for node.
        
        Args:
            node: Node to analyze
            duration_seconds: Total duration
            model_size_bytes: Model size
            
        Returns:
            float: Megabytes per second
        """
        if duration_seconds == 0 or not node.is_available():
            return 0.0
        
        bytes_per_second = node.get_communication_cost(model_size_bytes) / duration_seconds
        megabytes_per_second = bytes_per_second / (1024 * 1024)
        
        return float(megabytes_per_second)
    
    @staticmethod
    def compute_redundancy_ratio(num_nodes: int, num_rounds: int,
                                model_size_bytes: int = 512) -> float:
        """
        Compute communication redundancy.
        
        In federated learning, each node sends model to server,
        then server sends aggregated model back to all nodes.
        
        Redundancy = (num_nodes + 1) * num_rounds
        (one upload per node + one broadcast per round)
        
        Args:
            num_nodes: Number of participating nodes
            num_rounds: Number of federated rounds
            model_size_bytes: Model size
            
        Returns:
            float: Redundancy factor
        """
        if num_nodes == 0:
            return 0.0
        
        # Each round: num_nodes uploads + 1 aggregation + num_nodes downloads
        multiplier = (2 * num_nodes + 1)
        redundancy = float(multiplier * num_rounds)
        
        return redundancy
    
    @staticmethod
    def get_communication_summary(nodes: List[Node], num_rounds: int,
                                 model_size_bytes: int = 512) -> Dict[str, Any]:
        """
        Get comprehensive communication analysis.
        
        Args:
            nodes: List of nodes
            num_rounds: Number of federated rounds
            model_size_bytes: Model size
            
        Returns:
            Dictionary with all communication metrics
        """
        available_nodes = [n for n in nodes if n.is_available()]
        
        per_round = CommunicationMetrics.compute_per_round_overhead(
            nodes, num_rounds, model_size_bytes
        )
        
        total = per_round * num_rounds
        
        return {
            "per_round_bytes": float(per_round),
            "total_bytes": float(total),
            "total_megabytes": float(total / (1024 * 1024)),
            "communication_fairness": CommunicationMetrics.compute_communication_fairness(
                nodes, num_rounds, model_size_bytes
            ),
            "redundancy_factor": CommunicationMetrics.compute_redundancy_ratio(
                len(available_nodes), num_rounds, model_size_bytes
            ),
            "per_node_bytes": {
                node.node_id: CommunicationMetrics.compute_per_node_overhead(
                    node, num_rounds, model_size_bytes
                )
                for node in available_nodes
            }
        }
