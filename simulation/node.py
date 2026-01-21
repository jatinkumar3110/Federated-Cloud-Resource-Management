"""
Node Implementation Module
Represents heterogeneous nodes in federated cloud simulation.

Each node:
- Has a type (edge, user, compute, data center)
- Generates local workloads
- Participates as a federated client
- Tracks local metrics (energy, SLA, efficiency)

Responsibility: Node state management and local computation.
Called by: orchestration, strategies
"""

from typing import Dict, List, Tuple, Any
import numpy as np
from datetime import datetime

from simulation.node_types import NodeType, NodeProfile, get_node_profile


class Node:
    """
    Represents a heterogeneous node in federated cloud ecosystem.
    
    Attributes:
        node_id: Unique identifier
        node_type: Type of node (EDGE, USER, COMPUTE, DATA_CENTER)
        profile: Hardware profile for this type
        workload: Current workload [0, 100]
        cpu_utilization: Current CPU usage [0, 100]
        memory_utilization: Current memory usage [0, 100]
        is_online: Whether node is available
    """
    
    def __init__(self, node_id: int, node_type: NodeType, random_seed: int = 42):
        """
        Initialize node.
        
        Args:
            node_id: Unique node identifier
            node_type: Type of node (NodeType enum)
            random_seed: Seed for reproducible workload generation
        """
        self.node_id = node_id
        self.node_type = node_type
        self.profile = get_node_profile(node_type)
        
        # Random state
        np.random.seed(random_seed + node_id)
        self.random_seed = random_seed
        
        # Current state
        self.workload = 0.0
        self.cpu_utilization = 0.0
        self.memory_utilization = 0.0
        self.is_online = True
        
        # Metrics tracking
        self.energy_consumed = 0.0
        self.sla_violations = 0
        self.rounds_participated = 0
        self.total_training_time = 0.0
        
        # History for metrics
        self.history: List[Dict[str, Any]] = []
    
    # ========================================================================
    # WORKLOAD GENERATION
    # ========================================================================
    
    def generate_workload(self) -> float:
        """
        Generate local workload for this node.
        
        Respects node type constraints (max_workload).
        
        Returns:
            float: Workload value in [0, max_workload]
        """
        # Base workload with some variance
        base = np.random.uniform(0, self.profile.max_workload)
        noise = np.random.normal(0, self.profile.max_workload * 0.1)
        
        workload = np.clip(base + noise, 0, self.profile.max_workload)
        self.workload = float(workload)
        
        return self.workload
    
    def get_workload(self) -> float:
        """Get current workload without changing it."""
        return self.workload
    
    # ========================================================================
    # RESOURCE ALLOCATION & UTILIZATION
    # ========================================================================
    
    def allocate_resources(self, cpu_percent: float, memory_percent: float) -> Dict[str, float]:
        """
        Allocate and track resource utilization.
        
        Args:
            cpu_percent: CPU allocation [0, 100]
            memory_percent: Memory allocation [0, 100]
            
        Returns:
            Dictionary with actual allocation and metrics
        """
        # Respect node capacity constraints
        cpu_actual = np.clip(cpu_percent, 0, 100)
        memory_actual = np.clip(memory_percent, 0, 100)
        
        self.cpu_utilization = float(cpu_actual)
        self.memory_utilization = float(memory_actual)
        
        return {
            "cpu_allocated": cpu_actual,
            "memory_allocated": memory_actual,
            "cpu_capacity": self.profile.cpu_capacity,
            "memory_capacity": self.profile.memory_capacity
        }
    
    def get_resource_state(self) -> Dict[str, float]:
        """Get current resource utilization state."""
        return {
            "cpu_utilization": self.cpu_utilization,
            "memory_utilization": self.memory_utilization,
            "cpu_capacity": self.profile.cpu_capacity,
            "memory_capacity": self.profile.memory_capacity
        }
    
    # ========================================================================
    # ENERGY COMPUTATION
    # ========================================================================
    
    def compute_energy_consumption(self, duration_seconds: float = 1.0) -> float:
        """
        Compute energy consumed in this period.
        
        Model: energy = node_type_factor * (0.6*cpu + 0.4*memory) * duration
        
        Args:
            duration_seconds: Time period for energy computation
            
        Returns:
            float: Energy consumed (arbitrary units)
        """
        # Weighted combination of CPU and memory utilization
        normalized_cpu = self.cpu_utilization / 100.0
        normalized_mem = self.memory_utilization / 100.0
        
        util_score = 0.6 * normalized_cpu + 0.4 * normalized_mem
        
        # Apply node type energy factor
        energy = util_score * self.profile.energy_cost_factor * duration_seconds
        
        self.energy_consumed += energy
        return float(energy)
    
    def get_total_energy(self) -> float:
        """Get cumulative energy consumed."""
        return self.energy_consumed
    
    # ========================================================================
    # SLA COMPLIANCE
    # ========================================================================
    
    def check_sla_violation(self, cpu_threshold: float = 80.0, 
                            memory_threshold: float = 85.0) -> bool:
        """
        Check if node violates SLA constraints.
        
        Args:
            cpu_threshold: Max allowed CPU usage %
            memory_threshold: Max allowed memory usage %
            
        Returns:
            bool: True if violation detected
        """
        violation = (self.cpu_utilization > cpu_threshold or 
                    self.memory_utilization > memory_threshold)
        
        if violation:
            self.sla_violations += 1
        
        return violation
    
    def get_sla_violations(self) -> int:
        """Get count of SLA violations."""
        return self.sla_violations
    
    def get_sla_compliance_score(self) -> float:
        """
        Get SLA compliance score [0, 1].
        
        1.0 = no violations
        0.0 = all rounds violated
        
        Returns:
            float: Compliance score
        """
        if self.rounds_participated == 0:
            return 1.0
        
        compliance = 1.0 - (self.sla_violations / self.rounds_participated)
        return float(np.clip(compliance, 0.0, 1.0))
    
    # ========================================================================
    # AVAILABILITY & CONNECTIVITY
    # ========================================================================
    
    def check_availability(self) -> bool:
        """
        Check if node is available for this round.
        
        Models node failures/disconnections.
        
        Returns:
            bool: True if node is online
        """
        # Stochastic failure: check if this node should fail this round
        if np.random.random() < self.profile.failure_probability:
            self.is_online = False
        else:
            self.is_online = True
        
        return self.is_online
    
    def set_online(self, is_online: bool) -> None:
        """Manually set node availability."""
        self.is_online = bool(is_online)
    
    def is_available(self) -> bool:
        """Check if node is currently online."""
        return self.is_online
    
    # ========================================================================
    # FEDERATED PARTICIPATION
    # ========================================================================
    
    def participate_in_round(self, training_time: float) -> None:
        """
        Record node participation in a federated round.
        
        Args:
            training_time: Time spent training (seconds)
        """
        if self.is_online:
            self.rounds_participated += 1
            self.total_training_time += training_time
    
    def get_participation_stats(self) -> Dict[str, Any]:
        """Get participation statistics."""
        return {
            "rounds_participated": self.rounds_participated,
            "total_training_time": self.total_training_time,
            "avg_training_time": self.total_training_time / max(self.rounds_participated, 1),
            "availability_rate": self.rounds_participated / max(self.rounds_participated, 1)
        }
    
    # ========================================================================
    # COMMUNICATION OVERHEAD
    # ========================================================================
    
    def get_communication_cost(self, model_size_bytes: int = 512) -> int:
        """
        Get bytes transmitted in a federated round.
        
        Args:
            model_size_bytes: Size of model weights
            
        Returns:
            int: Bytes communicated
        """
        return self.profile.communication_cost * model_size_bytes
    
    def get_communication_overhead(self, num_rounds: int, model_size_bytes: int = 512) -> int:
        """
        Get total communication overhead.
        
        Args:
            num_rounds: Number of federated rounds
            model_size_bytes: Size of model weights
            
        Returns:
            int: Total bytes communicated
        """
        return self.get_communication_cost(model_size_bytes) * num_rounds
    
    # ========================================================================
    # METRICS & STATE TRACKING
    # ========================================================================
    
    def get_node_state(self) -> Dict[str, Any]:
        """
        Get current complete node state.
        
        Returns:
            Dictionary with all node attributes
        """
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "is_online": self.is_online,
            "workload": self.workload,
            "cpu_utilization": self.cpu_utilization,
            "memory_utilization": self.memory_utilization,
            "energy_consumed": self.energy_consumed,
            "sla_violations": self.sla_violations,
            "sla_compliance": self.get_sla_compliance_score(),
            "rounds_participated": self.rounds_participated
        }
    
    def log_state(self, round_num: int) -> Dict[str, Any]:
        """
        Log current state to history.
        
        Args:
            round_num: Federated round number
            
        Returns:
            Dictionary of logged state
        """
        state_entry = {
            "round": round_num,
            "timestamp": datetime.now().isoformat(),
            **self.get_node_state()
        }
        self.history.append(state_entry)
        return state_entry
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get complete state history."""
        return self.history.copy()
    
    def reset(self) -> None:
        """Reset node to initial state (for new experiment)."""
        self.workload = 0.0
        self.cpu_utilization = 0.0
        self.memory_utilization = 0.0
        self.is_online = True
        self.energy_consumed = 0.0
        self.sla_violations = 0
        self.rounds_participated = 0
        self.total_training_time = 0.0
        self.history = []
    
    # ========================================================================
    # HETEROGENEITY METRICS
    # ========================================================================
    
    def get_efficiency_score(self) -> float:
        """
        Get node efficiency: productivity per unit energy.
        
        Returns:
            float: Efficiency score [0, 1]
        """
        if self.energy_consumed == 0:
            return 1.0
        
        # Inverse of energy cost factor (lower cost = more efficient)
        energy_efficiency = 1.0 / self.profile.energy_cost_factor
        
        # Combine with SLA compliance
        sla_compliance = self.get_sla_compliance_score()
        
        efficiency = (energy_efficiency + sla_compliance) / 2.0
        return float(np.clip(efficiency, 0.0, 1.0))
    
    def get_capacity_utilization(self) -> float:
        """
        Get how much of node's maximum capacity is being used.
        
        Returns:
            float: Utilization rate [0, 1]
        """
        cpu_rate = self.cpu_utilization / 100.0
        mem_rate = self.memory_utilization / 100.0
        
        avg_utilization = (cpu_rate + mem_rate) / 2.0
        return float(np.clip(avg_utilization, 0.0, 1.0))
    
    def __repr__(self) -> str:
        """String representation of node."""
        return (f"Node(id={self.node_id}, type={self.node_type.value}, "
                f"online={self.is_online}, cpu={self.cpu_utilization:.1f}%, "
                f"mem={self.memory_utilization:.1f}%)")
