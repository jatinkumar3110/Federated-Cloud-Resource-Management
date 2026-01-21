"""
Simulation Layer: Workload Generation Module
Generates simulated cloud workloads for federated learning experiments.

Responsibility: Pure workload generation without side effects.
"""

import numpy as np
from typing import List, Dict, Tuple


class WorkloadGenerator:
    """
    Generates realistic cloud workloads for simulation.
    
    Attributes:
        intensity (float): Workload intensity factor [0, 1]
        variance (float): Variance in workload patterns
        random_seed (int): For reproducibility
    """
    
    def __init__(self, intensity: float = 0.5, variance: float = 0.2, random_seed: int = 42):
        """
        Initialize workload generator.
        
        Args:
            intensity: Base intensity multiplier for workloads
            variance: Variance factor for realistic fluctuations
            random_seed: Seed for reproducible results
        """
        if not (0 <= intensity <= 1):
            raise ValueError("Intensity must be between 0 and 1")
        
        self.intensity = intensity
        self.variance = variance
        self.random_seed = random_seed
        np.random.seed(random_seed)
        self.history: List[Dict] = []
    
    def generate_single_workload(self) -> float:
        """
        Generate a single workload value.
        
        Returns:
            float: Workload value in range [0, 100]
        """
        base = np.random.uniform(0, 100) * self.intensity
        noise = np.random.normal(0, self.variance * 10)
        workload = np.clip(base + noise, 0, 100)
        return float(workload)
    
    def generate_batch_workload(self, num_samples: int) -> List[float]:
        """
        Generate multiple workload samples.
        
        Args:
            num_samples: Number of workload samples to generate
            
        Returns:
            List of workload values
        """
        return [self.generate_single_workload() for _ in range(num_samples)]
    
    def get_workload_distribution(self, num_samples: int = 100) -> Dict[str, float]:
        """
        Analyze workload distribution.
        
        Args:
            num_samples: Number of samples for analysis
            
        Returns:
            Dictionary with statistical metrics
        """
        workloads = self.generate_batch_workload(num_samples)
        return {
            "mean": float(np.mean(workloads)),
            "std": float(np.std(workloads)),
            "min": float(np.min(workloads)),
            "max": float(np.max(workloads)),
            "median": float(np.median(workloads))
        }
    
    # ========================================================================
    # NEW: Normalization Helpers (Version 2.0)
    # ========================================================================
    
    @staticmethod
    def normalize_resource(value: float, max_value: float) -> float:
        """
        Normalize resource value to [0, 1] range.
        
        Args:
            value: Raw resource value (e.g., CPU %)
            max_value: Maximum expected value (e.g., 100 for %)
            
        Returns:
            float: Normalized value in [0, 1]
        """
        return float(np.clip(value / max_value, 0.0, 1.0))
    
    @staticmethod
    def normalize_batch(values: np.ndarray, max_value: float) -> np.ndarray:
        """
        Normalize batch of resource values to [0, 1].
        
        Args:
            values: Array of resource values
            max_value: Maximum expected value
            
        Returns:
            np.ndarray: Normalized values in [0, 1]
        """
        return np.clip(values / max_value, 0.0, 1.0)
    
    @staticmethod
    def normalize_resources(cpu: float, memory: float, disk: float, 
                           workload: float) -> Tuple[float, float, float, float]:
        """
        Normalize all resource metrics to [0, 1].
        
        Args:
            cpu: CPU usage [0, 100]
            memory: Memory usage [0, 100]
            disk: Disk usage [0, 100]
            workload: Workload value [0, 100]
            
        Returns:
            Tuple of normalized values (cpu, memory, disk, workload)
        """
        cpu_norm = WorkloadGenerator.normalize_resource(cpu, 100.0)
        mem_norm = WorkloadGenerator.normalize_resource(memory, 100.0)
        disk_norm = WorkloadGenerator.normalize_resource(disk, 100.0)
        wl_norm = WorkloadGenerator.normalize_resource(workload, 100.0)
        
        return (cpu_norm, mem_norm, disk_norm, wl_norm)
    
    def reset_history(self) -> None:
        """Clear workload history."""
        self.history = []
