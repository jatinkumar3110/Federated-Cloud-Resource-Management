"""
Simulation Layer: Resource Monitoring Module
Monitors and tracks system resource metrics.

Responsibility: Collect and return resource metrics without side effects.
"""

import psutil
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime


class ResourceMonitor:
    """
    Monitors system resource utilization and computes system-level metrics.
    
    Attributes:
        metrics_history (List): Historical metrics snapshots
    """
    
    def __init__(self):
        """Initialize resource monitor."""
        self.metrics_history: List[Dict] = []
    
    def get_cpu_usage(self) -> float:
        """
        Get current CPU usage percentage.
        
        Returns:
            float: CPU usage in range [0, 100]
        """
        return float(psutil.cpu_percent(interval=0.5))
    
    def get_memory_usage(self) -> float:
        """
        Get current memory usage percentage.
        
        Returns:
            float: Memory usage in range [0, 100]
        """
        return float(psutil.virtual_memory().percent)
    
    def get_disk_usage(self) -> float:
        """
        Get current disk usage percentage.
        
        Returns:
            float: Disk usage in range [0, 100]
        """
        return float(psutil.disk_usage('/').percent)
    
    def collect_metrics(self) -> Dict[str, float]:
        """
        Collect all resource metrics in a single snapshot.
        
        Returns:
            Dictionary with timestamp and resource metrics
        """
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": self.get_cpu_usage(),
            "memory": self.get_memory_usage(),
            "disk": self.get_disk_usage()
        }
        self.metrics_history.append(metrics)
        return metrics
    
    def get_average_metrics(self, window_size: int = 5) -> Dict[str, float]:
        """
        Get average metrics over recent window.
        
        Args:
            window_size: Number of recent samples to average
            
        Returns:
            Dictionary with averaged metrics
        """
        if not self.metrics_history:
            return {"cpu": 0.0, "memory": 0.0, "disk": 0.0}
        
        recent = self.metrics_history[-window_size:]
        return {
            "cpu": float(np.mean([m["cpu"] for m in recent])),
            "memory": float(np.mean([m["memory"] for m in recent])),
            "disk": float(np.mean([m["disk"] for m in recent]))
        }
    
    def clear_history(self) -> None:
        """Clear metrics history."""
        self.metrics_history = []
    
    # ========================================================================
    # NEW: System-Level Metric Computation (Version 2.0)
    # ========================================================================
    
    def compute_energy(self, cpu_usage: float, memory_usage: float) -> float:
        """
        Compute energy consumption as proxy.
        
        Energy ∝ CPU + Memory utilization (normalized).
        Lower is better.
        
        Args:
            cpu_usage: CPU percentage [0, 100]
            memory_usage: Memory percentage [0, 100]
            
        Returns:
            float: Energy consumption score [0, 1]
        """
        cpu_norm = cpu_usage / 100.0
        mem_norm = memory_usage / 100.0
        energy = (cpu_norm * 0.6) + (mem_norm * 0.4)
        return float(np.clip(energy, 0.0, 1.0))
    
    def compute_resource_imbalance(self, cpu_usage: float, 
                                   memory_usage: float) -> float:
        """
        Compute resource utilization imbalance.
        
        imbalance = |cpu - memory| / 100
        Lower is better (balanced resources).
        
        Args:
            cpu_usage: CPU percentage [0, 100]
            memory_usage: Memory percentage [0, 100]
            
        Returns:
            float: Imbalance score [0, 1]
        """
        imbalance = abs(cpu_usage - memory_usage) / 100.0
        return float(np.clip(imbalance, 0.0, 1.0))
    
    def compute_sla_penalty(self, cpu_usage: float, 
                            memory_usage: float,
                            sla_cpu_threshold: float = 80.0,
                            sla_memory_threshold: float = 85.0) -> float:
        """
        Compute SLA compliance penalty.
        
        penalty = 1 if (cpu > threshold OR memory > threshold) else 0
        Lower is better (no violations).
        
        Args:
            cpu_usage: CPU percentage [0, 100]
            memory_usage: Memory percentage [0, 100]
            sla_cpu_threshold: CPU SLA threshold
            sla_memory_threshold: Memory SLA threshold
            
        Returns:
            float: SLA penalty [0, 1]
        """
        if cpu_usage > sla_cpu_threshold or memory_usage > sla_memory_threshold:
            return 1.0
        return 0.0
    
    def compute_system_optimization_score(self, 
                                         cpu_usage: float,
                                         memory_usage: float,
                                         alpha: float = 0.4,
                                         beta: float = 0.35,
                                         gamma: float = 0.25,
                                         sla_cpu: float = 80.0,
                                         sla_mem: float = 85.0) -> Dict[str, float]:
        """
        Compute overall system optimization score.
        
        score = α*energy + β*imbalance + γ*sla_penalty
        
        Args:
            cpu_usage: CPU percentage [0, 100]
            memory_usage: Memory percentage [0, 100]
            alpha: Weight for energy (default 0.4)
            beta: Weight for imbalance (default 0.35)
            gamma: Weight for SLA (default 0.25)
            sla_cpu: CPU SLA threshold
            sla_mem: Memory SLA threshold
            
        Returns:
            Dictionary with components and total score
        """
        energy = self.compute_energy(cpu_usage, memory_usage)
        imbalance = self.compute_resource_imbalance(cpu_usage, memory_usage)
        sla_penalty = self.compute_sla_penalty(cpu_usage, memory_usage, sla_cpu, sla_mem)
        
        total_score = (alpha * energy) + (beta * imbalance) + (gamma * sla_penalty)
        
        return {
            "energy": float(energy),
            "imbalance": float(imbalance),
            "sla_penalty": float(sla_penalty),
            "total_score": float(np.clip(total_score, 0.0, 1.0))
        }


# Import numpy for averaging function
import numpy as np
