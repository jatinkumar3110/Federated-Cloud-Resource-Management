"""
Metrics & Evaluation Layer: Performance Evaluation Module
Computes metrics and logs results for analysis.

Responsibility: Metric computation and logging without execution logic.
UPDATED (v2.0): Added system-level metrics (energy, SLA, efficiency)
"""

import csv
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import os


class MetricsEvaluator:
    """
    Evaluates model and resource metrics.
    
    UPDATED (v2.0):
    - Added system-level metrics computation
    - Tracks energy, SLA violations, efficiency
    
    Responsibility: Pure metric computation without side effects.
    """
    
    def __init__(self, log_file: str = 'logs/metrics_log.csv'):
        """
        Initialize metrics evaluator.
        
        Args:
            log_file: Path to CSV log file
        """
        self.log_file = log_file
        self.metrics_buffer: List[Dict] = []
    
    def compute_mse(self, predictions: np.ndarray, targets: np.ndarray) -> float:
        """
        Compute Mean Squared Error.
        
        Args:
            predictions: Model predictions
            targets: Ground truth targets
            
        Returns:
            MSE value
        """
        if predictions.shape != targets.shape:
            raise ValueError("Predictions and targets must have same shape")
        
        mse = np.mean((predictions - targets) ** 2)
        return float(mse)
    
    def compute_mae(self, predictions: np.ndarray, targets: np.ndarray) -> float:
        """
        Compute Mean Absolute Error.
        
        Args:
            predictions: Model predictions
            targets: Ground truth targets
            
        Returns:
            MAE value
        """
        mae = np.mean(np.abs(predictions - targets))
        return float(mae)
    
    def compute_r2_score(self, predictions: np.ndarray, targets: np.ndarray) -> float:
        """
        Compute R² coefficient of determination.
        
        Args:
            predictions: Model predictions
            targets: Ground truth targets
            
        Returns:
            R² score [0, 1]
        """
        ss_res = np.sum((targets - predictions) ** 2)
        ss_tot = np.sum((targets - np.mean(targets)) ** 2)
        
        if ss_tot == 0:
            return 0.0
        
        r2 = 1 - (ss_res / ss_tot)
        return float(np.clip(r2, 0, 1))
    
    def compute_resource_efficiency(self, 
                                   cpu: float, memory: float, 
                                   model_accuracy: float) -> float:
        """
        Compute resource efficiency metric.
        
        Formula: Efficiency = Model Accuracy / (CPU + Memory)
        
        Args:
            cpu: CPU usage percentage
            memory: Memory usage percentage
            model_accuracy: Model accuracy score [0, 1]
            
        Returns:
            Efficiency metric
        """
        denominator = (cpu + memory) / 100.0
        if denominator == 0:
            return 0.0
        
        efficiency = model_accuracy / denominator
        return float(efficiency)
    
    def log_metrics_to_csv(self, metrics: Dict) -> None:
        """
        Log metrics to CSV file.
        
        Args:
            metrics: Dictionary of metric key-value pairs
        """
        # Add timestamp if not present
        if "timestamp" not in metrics:
            metrics["timestamp"] = datetime.now().isoformat()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.log_file) or '.', exist_ok=True)
        
        # Check if file exists
        file_exists = os.path.isfile(self.log_file)
        
        # Write to CSV
        try:
            with open(self.log_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = list(metrics.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(metrics)
        except IOError as e:
            print(f"Warning: Could not write to {self.log_file}: {e}")
    
    def compute_federated_metrics(self, client_losses: List[float]) -> Dict[str, float]:
        """
        Compute aggregated federated learning metrics.
        
        Args:
            client_losses: List of losses from each client
            
        Returns:
            Dictionary with aggregated metrics
        """
        if not client_losses:
            return {"avg_loss": 0.0, "std_loss": 0.0, "min_loss": 0.0, "max_loss": 0.0}
        
        client_losses_arr = np.array(client_losses)
        return {
            "avg_loss": float(np.mean(client_losses_arr)),
            "std_loss": float(np.std(client_losses_arr)),
            "min_loss": float(np.min(client_losses_arr)),
            "max_loss": float(np.max(client_losses_arr))
        }
    
    def compute_sla_compliance(self, 
                              response_time: float, 
                              sla_threshold: float = 1.0) -> Tuple[bool, float]:
        """
        Check SLA (Service Level Agreement) compliance.
        
        Args:
            response_time: Response time in seconds
            sla_threshold: SLA threshold in seconds
            
        Returns:
            Tuple of (is_compliant, compliance_percentage)
        """
        is_compliant = response_time <= sla_threshold
        compliance_percentage = max(0, 100 * (1 - response_time / sla_threshold))
        
        return (is_compliant, float(compliance_percentage))
    
    # ========================================================================
    # NEW: System-Level Metrics (Version 2.0)
    # ========================================================================
    
    def compute_system_energy(self, cpu_avg: float, memory_avg: float) -> float:
        """
        Compute average energy consumption across rounds.
        
        Args:
            cpu_avg: Average CPU usage (%)
            memory_avg: Average memory usage (%)
            
        Returns:
            Energy score [0, 1] - lower is better
        """
        from simulation.resource_monitor import ResourceMonitor
        monitor = ResourceMonitor()
        energy = monitor.compute_energy(cpu_avg, memory_avg)
        return float(energy)
    
    def compute_sla_violations(self, cpu_values: List[float], 
                               memory_values: List[float],
                               sla_cpu: float = 80.0,
                               sla_mem: float = 85.0) -> Dict[str, float]:
        """
        Count and report SLA violations across rounds.
        
        Args:
            cpu_values: List of CPU usage values per round
            memory_values: List of memory usage values per round
            sla_cpu: CPU SLA threshold (%)
            sla_mem: Memory SLA threshold (%)
            
        Returns:
            Dictionary with violation counts and rates
        """
        cpu_violations = sum(1 for cpu in cpu_values if cpu > sla_cpu)
        mem_violations = sum(1 for mem in memory_values if mem > sla_mem)
        total_rounds = max(len(cpu_values), len(memory_values))
        
        violation_rate = (cpu_violations + mem_violations) / (2 * total_rounds) if total_rounds > 0 else 0.0
        
        return {
            "cpu_violations": int(cpu_violations),
            "memory_violations": int(mem_violations),
            "total_violations": int(cpu_violations + mem_violations),
            "violation_rate": float(violation_rate)
        }
    
    def compute_resource_efficiency(self, cpu_values: List[float],
                                   memory_values: List[float],
                                   disk_values: List[float]) -> float:
        """
        Compute overall resource utilization efficiency.
        
        Efficiency = 1 - (variance / mean)
        Higher is better (balanced utilization).
        
        Args:
            cpu_values: CPU usage per round
            memory_values: Memory usage per round
            disk_values: Disk usage per round
            
        Returns:
            Efficiency score [0, 1]
        """
        all_values = np.array(cpu_values + memory_values + disk_values)
        
        if len(all_values) == 0 or np.mean(all_values) == 0:
            return 0.0
        
        mean = np.mean(all_values)
        variance = np.var(all_values)
        
        # Efficiency: balance between resources (lower variance = better)
        efficiency = np.clip(1.0 - (variance / (mean * mean + 1e-6)), 0.0, 1.0)
        return float(efficiency)
    
    def compute_training_stability(self, losses: List[float]) -> float:
        """
        Measure training stability (smoother curve = stable).
        
        Stability = 1 - (std_dev / mean)
        Higher is more stable.
        
        Args:
            losses: Loss values across rounds
            
        Returns:
            Stability score [0, 1]
        """
        if len(losses) < 2 or np.mean(losses) == 0:
            return 0.0
        
        std_dev = np.std(losses)
        mean = np.mean(losses)
        
        stability = np.clip(1.0 - (std_dev / (mean + 1e-6)), 0.0, 1.0)
        return float(stability)
