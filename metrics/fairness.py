"""
Fairness Metrics Module
Measures fairness of resource allocation across heterogeneous nodes.

Research question: Does federated approach distribute resources more fairly
across different node types compared to centralized?

Responsibility: Compute fairness indices, no execution.
"""

from typing import List, Dict, Any
import numpy as np
from simulation.node import Node


class FairnessMetrics:
    """
    Computes fairness metrics for resource allocation.
    
    Fairness definitions:
    - Jain's Index: How evenly resources are distributed [0, 1]
    - Gini Coefficient: Income inequality metric [0, 1]
    - Allocation Gap: Max-min allocation difference
    - Type-wise Balance: Fairness within each node type
    """
    
    @staticmethod
    def compute_jain_index(allocations: List[float]) -> float:
        """
        Compute Jain's Fairness Index.
        
        J(x) = (sum(x_i))^2 / (n * sum(x_i^2))
        
        Perfect equality: J = 1.0
        Perfect inequality: J -> 1/n
        
        Args:
            allocations: List of resource allocations
            
        Returns:
            float: Jain index in [1/n, 1]
        """
        if len(allocations) == 0:
            return 1.0
        
        allocations = np.array(allocations, dtype=float)
        allocations = np.clip(allocations, 0, None)  # Ensure non-negative
        
        if np.sum(allocations) == 0:
            return 1.0
        
        n = len(allocations)
        numerator = np.sum(allocations) ** 2
        denominator = n * np.sum(allocations ** 2)
        
        jain_index = float(numerator / denominator)
        return np.clip(jain_index, 1/n, 1.0)
    
    @staticmethod
    def compute_gini_coefficient(allocations: List[float]) -> float:
        """
        Compute Gini Coefficient (income inequality).
        
        G = (2 * sum(i * x_i)) / (n * sum(x_i)) - (n+1)/n
        
        No inequality: G = 0.0
        Complete inequality: G = 1.0
        
        Args:
            allocations: List of resource allocations
            
        Returns:
            float: Gini coefficient in [0, 1]
        """
        if len(allocations) == 0:
            return 0.0
        
        allocations = np.array(allocations, dtype=float)
        allocations = np.sort(allocations)  # Sort required
        
        if np.sum(allocations) == 0:
            return 0.0
        
        n = len(allocations)
        indices = np.arange(1, n + 1)
        
        numerator = 2 * np.sum(indices * allocations)
        denominator = n * np.sum(allocations)
        
        gini = (numerator / denominator) - (n + 1) / n
        return float(np.clip(gini, 0.0, 1.0))
    
    @staticmethod
    def compute_allocation_gap(allocations: List[float]) -> float:
        """
        Compute allocation gap (max - min).
        
        Smaller gap = more fair.
        
        Args:
            allocations: List of resource allocations
            
        Returns:
            float: Gap between max and min allocation
        """
        if len(allocations) == 0:
            return 0.0
        
        allocations = np.array(allocations, dtype=float)
        
        if np.sum(allocations) == 0:
            return 0.0
        
        gap = float(np.max(allocations) - np.min(allocations))
        return gap
    
    @staticmethod
    def compute_coefficient_of_variation(allocations: List[float]) -> float:
        """
        Compute coefficient of variation (std / mean).
        
        Lower CV = more fair (less variation).
        
        Args:
            allocations: List of resource allocations
            
        Returns:
            float: Coefficient of variation in [0, inf]
        """
        if len(allocations) == 0:
            return 0.0
        
        allocations = np.array(allocations, dtype=float)
        
        mean = np.mean(allocations)
        if mean == 0:
            return 0.0
        
        std = np.std(allocations)
        cv = float(std / mean)
        return cv
    
    @staticmethod
    def compute_type_wise_fairness(nodes: List[Node]) -> Dict[str, float]:
        """
        Compute fairness metrics within each node type.
        
        Useful for understanding if certain node types are disadvantaged.
        
        Args:
            nodes: List of nodes to analyze
            
        Returns:
            Dictionary mapping node_type -> fairness_score [0, 1]
        """
        # Group nodes by type
        nodes_by_type: Dict[str, List[Node]] = {}
        for node in nodes:
            node_type = node.node_type.value
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node)
        
        # Compute fairness within each type
        fairness_by_type: Dict[str, float] = {}
        for node_type, nodes_of_type in nodes_by_type.items():
            allocations = [n.cpu_utilization for n in nodes_of_type]
            jain = FairnessMetrics.compute_jain_index(allocations)
            fairness_by_type[node_type] = jain
        
        return fairness_by_type
    
    @staticmethod
    def compute_fairness_score(nodes: List[Node]) -> float:
        """
        Compute overall fairness score [0, 1].
        
        Combines multiple fairness metrics into single score.
        
        Args:
            nodes: List of nodes
            
        Returns:
            float: Overall fairness in [0, 1]
        """
        allocations = [n.cpu_utilization for n in nodes if n.is_available()]
        
        if len(allocations) == 0:
            return 1.0
        
        # Use Jain's index as primary fairness metric
        jain = FairnessMetrics.compute_jain_index(allocations)
        
        # Penalize very high variation
        cv = FairnessMetrics.compute_coefficient_of_variation(allocations)
        cv_penalty = np.clip(cv / 2.0, 0, 0.3)  # Max penalty 0.3
        
        fairness = jain * (1.0 - cv_penalty)
        return float(np.clip(fairness, 0.0, 1.0))
    
    @staticmethod
    def get_fairness_summary(nodes: List[Node]) -> Dict[str, Any]:
        """
        Get comprehensive fairness analysis.
        
        Args:
            nodes: List of nodes
            
        Returns:
            Dictionary with all fairness metrics
        """
        allocations = [n.cpu_utilization for n in nodes if n.is_available()]
        
        if len(allocations) == 0:
            allocations = [0.0]
        
        return {
            "jain_index": FairnessMetrics.compute_jain_index(allocations),
            "gini_coefficient": FairnessMetrics.compute_gini_coefficient(allocations),
            "allocation_gap": FairnessMetrics.compute_allocation_gap(allocations),
            "coefficient_of_variation": FairnessMetrics.compute_coefficient_of_variation(allocations),
            "overall_fairness": FairnessMetrics.compute_fairness_score(nodes),
            "type_wise_fairness": FairnessMetrics.compute_type_wise_fairness(nodes)
        }
