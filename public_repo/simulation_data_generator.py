"""
Realistic Simulation Data Generator
====================================
Generates research-grade simulation data for federated learning scenarios.

Key Improvements:
1. Per-node energy calculation based on CPU/memory utilization
2. Communication overhead for federated learning (MB per round)
3. Fairness variance across strategies (not uniform)
4. Carbon footprint = energy × regional carbon intensity
5. NaN guards throughout
6. Semantic correctness (convergence_metric vs loss)

Author: Dashboard System
Date: 2026-01-22
"""

import math
import numpy as np
from typing import Dict, List, Any


class RealisticSimulationGenerator:
    """
    Generates realistic simulation results with proper data semantics.
    """
    
    # Carbon intensity by region (kg CO2/kWh)
    CARBON_INTENSITY = {
        'clean': 0.05,      # Renewable-heavy regions
        'mixed': 0.35,      # Grid mix
        'fossil': 0.85      # Coal-heavy regions
    }
    
    # Node energy profiles (base power in watts)
    NODE_POWER_BASE = {
        'EDGE_DEVICE': 5,           # Low power
        'USER_DEVICE': 3,            # Very low power
        'COMPUTE_SERVER': 200,       # Medium power
        'DATA_CENTER_NODE': 500      # High power
    }
    
    # Communication overhead per node per round (MB)
    COMM_OVERHEAD_MB = {
        'EDGE_DEVICE': 2.5,
        'USER_DEVICE': 1.5,
        'COMPUTE_SERVER': 8,
        'DATA_CENTER_NODE': 12
    }
    
    # Strategy fairness profiles (base score ± variance)
    STRATEGY_FAIRNESS = {
        'Static Allocation': {'base': 0.65, 'variance': 0.08},
        'Centralized ML': {'base': 0.72, 'variance': 0.06},
        'Federated Learning': {'base': 0.85, 'variance': 0.04},
        'Energy-Aware Heuristic': {'base': 0.78, 'variance': 0.07}
    }
    
    # Strategy convergence profiles (convergence metric = inverse of loss)
    STRATEGY_CONVERGENCE = {
        'Static Allocation': {'start': 0.3, 'decay': 0.05},
        'Centralized ML': {'start': 0.45, 'decay': 0.08},
        'Federated Learning': {'start': 0.40, 'decay': 0.07},
        'Energy-Aware Heuristic': {'start': 0.35, 'decay': 0.06}
    }
    
    def __init__(self, nodes: List[Dict], num_rounds: int = 5, strategy: str = 'Federated Learning'):
        """
        Initialize generator.
        
        Args:
            nodes: List of node dicts with type, cpu_cores, memory_gb, region
            num_rounds: Number of simulation rounds
            strategy: Strategy name
        """
        self.nodes = nodes or []
        self.num_rounds = max(1, min(num_rounds, 20))  # Guard: 1-20 rounds
        self.strategy = strategy or 'Federated Learning'
        self.num_clients = len(nodes)
        
    def _safe_value(self, value: float, default: float = 0.0, min_val: float = None, max_val: float = None) -> float:
        """
        Guard against NaN/inf values.
        
        Args:
            value: Value to validate
            default: Default if invalid
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            Safe float value
        """
        if value is None or math.isnan(value) or math.isinf(value):
            return default
        if min_val is not None and value < min_val:
            return min_val
        if max_val is not None and value > max_val:
            return max_val
        return float(value)
    
    def _calculate_node_energy(self, node: Dict, cpu_utilization: float) -> float:
        """
        Calculate energy consumption for a node.
        
        Energy formula: base_power × (0.3 + 0.7 × cpu_utilization) × cpu_cores / 8
        This accounts for both baseline and utilization-based consumption.
        
        Args:
            node: Node configuration dict
            cpu_utilization: CPU utilization 0-1
            
        Returns:
            Energy in kWh (safe value)
        """
        try:
            node_type = node.get('type', 'COMPUTE_SERVER')
            base_power = self.NODE_POWER_BASE.get(node_type, 50)  # watts
            cpu_cores = node.get('cpu_cores', 4)
            
            # Utilization-aware power: baseline (30%) + load-dependent (70%)
            cpu_util_safe = self._safe_value(cpu_utilization, 0.5, 0, 1)
            power_watts = base_power * (0.3 + 0.7 * cpu_util_safe) * (cpu_cores / 8)
            
            # Convert to kWh (1 hour simulation)
            energy_kwh = power_watts / 1000.0
            
            return self._safe_value(energy_kwh, 0.1, 0.001)
        except Exception as e:
            print(f"Energy calculation error: {e}")
            return 0.1  # Safe default
    
    def _calculate_communication(self) -> float:
        """
        Calculate total communication for all nodes in a round (MB).
        
        For federated learning: 2 × sum(per-node overhead) 
        (upstream model + downstream weights)
        
        Returns:
            Communication in MB (safe value)
        """
        try:
            total_mb = 0
            for node in self.nodes:
                node_type = node.get('type', 'COMPUTE_SERVER')
                overhead = self.COMM_OVERHEAD_MB.get(node_type, 4)
                total_mb += overhead * 2  # Upstream + downstream
            
            return self._safe_value(total_mb, 10, 1)
        except Exception as e:
            print(f"Communication calculation error: {e}")
            return 10.0
    
    def _calculate_fairness(self, round_num: int) -> float:
        """
        Calculate fairness score for strategy.
        
        Fairness with controlled variance (federated typically better).
        Converges upward as rounds progress (learning stabilizes fairness).
        
        Args:
            round_num: Round number (1-indexed)
            
        Returns:
            Fairness score 0-1 (safe value)
        """
        try:
            profile = self.STRATEGY_FAIRNESS.get(self.strategy, {'base': 0.75, 'variance': 0.05})
            base = profile['base']
            variance = profile['variance']
            
            # Add round-dependent improvement (fairness converges)
            improvement = (round_num / self.num_rounds) * 0.1
            
            # Random variance
            np.random.seed(hash(f"{self.strategy}_{round_num}") % 2**32)
            noise = np.random.normal(0, variance)
            
            fairness = base + improvement + noise
            
            return self._safe_value(fairness, 0.75, 0.0, 1.0)
        except Exception as e:
            print(f"Fairness calculation error: {e}")
            return 0.75
    
    def _calculate_convergence(self, round_num: int) -> float:
        """
        Calculate convergence metric (objective quality, inverse of loss).
        
        Higher = better convergence. Uses strategy-specific profiles.
        Not named 'loss' to avoid confusion with error metrics.
        
        Args:
            round_num: Round number (1-indexed)
            
        Returns:
            Convergence metric 0-1 (safe value)
        """
        try:
            profile = self.STRATEGY_CONVERGENCE.get(self.strategy, {'start': 0.4, 'decay': 0.06})
            start = profile['start']
            decay = profile['decay']
            
            # Exponential convergence toward 1.0
            convergence = 1.0 - (1.0 - start) * math.exp(-decay * round_num)
            
            return self._safe_value(convergence, 0.5, 0.0, 1.0)
        except Exception as e:
            print(f"Convergence calculation error: {e}")
            return 0.5
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate complete simulation results.
        
        Returns:
            Dict with final_metrics, round_results, and metadata
        """
        round_results = []
        total_energy = 0.0
        total_communication = 0.0
        fairness_scores = []
        convergence_scores = []
        sla_violations = 0
        
        # Simulate each round
        for round_num in range(1, self.num_rounds + 1):
            # Per-round energy (variable CPU utilization)
            round_energy = 0.0
            for node in self.nodes:
                # Utilization decreases as learning converges (more idle time)
                base_util = 0.7
                convergence_impact = 0.3 * ((round_num - 1) / self.num_rounds)
                cpu_util = base_util - convergence_impact + np.random.normal(0, 0.05)
                cpu_util = self._safe_value(cpu_util, 0.5, 0.1, 0.95)
                
                node_energy = self._calculate_node_energy(node, cpu_util)
                round_energy += node_energy
            
            # Communication for this round
            round_comm = self._calculate_communication()
            
            # Fairness and convergence for this round
            fairness = self._calculate_fairness(round_num)
            convergence = self._calculate_convergence(round_num)
            
            # SLA violations (occasional, strategy-dependent)
            sla_prob = {'Federated Learning': 0.05, 'Energy-Aware Heuristic': 0.08}.get(self.strategy, 0.1)
            round_sla = 1 if np.random.random() < sla_prob else 0
            
            # Accumulate
            total_energy += round_energy
            total_communication += round_comm
            fairness_scores.append(fairness)
            convergence_scores.append(convergence)
            sla_violations += round_sla
            
            # Round result
            round_results.append({
                'round': round_num,
                'energy_used': self._safe_value(round_energy, 0.1),
                'communication_mb': self._safe_value(round_comm, 5),
                'convergence_metric': self._safe_value(convergence, 0.5),  # Renamed from loss
                'fairness_score': self._safe_value(fairness, 0.75),
                'sla_violations': round_sla,
                'avg_client_loss': self._safe_value(1.0 - convergence, 0.5),  # For backwards compat
                'global_loss': self._safe_value(1.0 - convergence * 0.9, 0.5)
            })
        
        # Aggregate metrics with guards
        avg_energy = self._safe_value(total_energy / self.num_rounds, 0.1)
        avg_fairness = self._safe_value(np.mean(fairness_scores), 0.75, 0, 1)
        avg_convergence = self._safe_value(np.mean(convergence_scores), 0.5, 0, 1)
        
        # Energy mix by node regions
        energy_by_region = {}
        for node in self.nodes:
            region = node.get('region', 'mixed')
            if region not in energy_by_region:
                energy_by_region[region] = 0
            energy_by_region[region] += total_energy / len(self.nodes)
        
        # Carbon footprint = energy × regional intensity
        carbon_kg = 0.0
        for region, energy in energy_by_region.items():
            intensity = self.CARBON_INTENSITY.get(region, 0.35)
            carbon_kg += energy * intensity
        
        return {
            'final_metrics': {
                'avg_energy': avg_energy,
                'total_energy': self._safe_value(total_energy, 1.0),
                'energy_std': self._safe_value(np.std([r['energy_used'] for r in round_results]), 0.1),
                'fairness_score': avg_fairness,
                'convergence_metric': avg_convergence,
                'sla_violations': int(sla_violations),
                'communication_mb': self._safe_value(total_communication / self.num_rounds, 5),
                'carbon_footprint_kg': self._safe_value(carbon_kg, 1.0),
                'green_score': self._safe_value(1.0 - (carbon_kg / (total_energy * 1.0 + 0.1)) * 0.3, 0.7, 0, 1)
            },
            'round_results': round_results,
            'energy_by_region': {k: self._safe_value(v, 0.1) for k, v in energy_by_region.items()},
            'num_clients': len(self.nodes),
            'simulation': {
                'strategy': self.strategy,
                'num_nodes': len(self.nodes),
                'num_rounds': self.num_rounds,
                'node_types': list(set(n.get('type', 'UNKNOWN') for n in self.nodes))
            }
        }
