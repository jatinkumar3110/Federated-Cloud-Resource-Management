"""
Node Types Definition Module
Defines heterogeneous node/device profiles for cloud simulation.

Simulates realistic diversity in federated cloud ecosystems:
- Edge devices (limited resources, high latency)
- User devices (mobile, variable capacity)
- Compute servers (medium-high resources)
- Data center nodes (maximum resources, optimized)

Responsibility: Define node type profiles and constants only.
Called by: simulation.node
"""

from enum import Enum
from typing import Dict, Any


class NodeType(Enum):
    """Enumeration of heterogeneous node types in cloud ecosystem."""
    EDGE_DEVICE = "edge_device"
    USER_DEVICE = "user_device"
    COMPUTE_SERVER = "compute_server"
    DATA_CENTER_NODE = "data_center_node"


class NodeProfile:
    """
    Defines hardware and behavioral characteristics of a node type.
    
    Attributes:
        cpu_capacity: Number of CPU cores
        memory_capacity: RAM in GB
        energy_cost_factor: Relative energy consumption multiplier (1.0 = baseline)
        sla_sensitivity: How much node cares about SLA violations [0, 1]
        communication_cost: Bytes per federated round
        failure_probability: Likelihood of node dropout [0, 1]
        max_workload: Maximum workload intensity this node can handle [0, 100]
    """
    
    def __init__(self, cpu_capacity: int, memory_capacity: float, 
                 energy_cost_factor: float, sla_sensitivity: float,
                 communication_cost: int, failure_probability: float = 0.0,
                 max_workload: float = 100.0):
        """Initialize node profile."""
        self.cpu_capacity = cpu_capacity
        self.memory_capacity = memory_capacity
        self.energy_cost_factor = energy_cost_factor
        self.sla_sensitivity = sla_sensitivity
        self.communication_cost = communication_cost
        self.failure_probability = failure_probability
        self.max_workload = max_workload
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "cpu_capacity": self.cpu_capacity,
            "memory_capacity": self.memory_capacity,
            "energy_cost_factor": self.energy_cost_factor,
            "sla_sensitivity": self.sla_sensitivity,
            "communication_cost": self.communication_cost,
            "failure_probability": self.failure_probability,
            "max_workload": self.max_workload
        }


# ============================================================================
# NODE TYPE PROFILES: Real-world inspired specifications
# ============================================================================

NODE_PROFILES: Dict[NodeType, NodeProfile] = {
    # Edge devices: IoT, edge servers at network periphery
    # Characteristics: Low resources, high latency, always-on SLA demands
    NodeType.EDGE_DEVICE: NodeProfile(
        cpu_capacity=2,              # 2 cores (limited processing)
        memory_capacity=4.0,         # 4 GB RAM
        energy_cost_factor=0.8,      # Efficient (battery-powered or solar)
        sla_sensitivity=0.9,         # Very strict about availability
        communication_cost=512,      # Small payload, low bandwidth
        failure_probability=0.05,    # Occasional disconnects
        max_workload=20.0            # Limited capacity
    ),
    
    # User devices: Smartphones, laptops, tablets
    # Characteristics: Heterogeneous, variable connectivity, power-aware
    NodeType.USER_DEVICE: NodeProfile(
        cpu_capacity=4,              # 4 cores (modern mobile/laptop)
        memory_capacity=8.0,         # 8 GB RAM
        energy_cost_factor=1.2,      # Higher cost (mobile battery impact)
        sla_sensitivity=0.7,         # Moderate SLA expectations
        communication_cost=1024,     # Medium payload
        failure_probability=0.08,    # Intermittent connectivity
        max_workload=40.0            # Moderate capacity
    ),
    
    # Compute servers: On-premises servers, private cloud
    # Characteristics: Dedicated resources, reliable, medium-high capacity
    NodeType.COMPUTE_SERVER: NodeProfile(
        cpu_capacity=16,             # 16 cores (server-grade)
        memory_capacity=32.0,        # 32 GB RAM
        energy_cost_factor=1.0,      # Baseline energy cost
        sla_sensitivity=0.5,         # Moderate SLA expectations
        communication_cost=2048,     # Larger payload, better network
        failure_probability=0.02,    # Rare failures
        max_workload=80.0            # High capacity
    ),
    
    # Data center nodes: Cloud provider infrastructure
    # Characteristics: Maximum resources, optimized, high availability
    NodeType.DATA_CENTER_NODE: NodeProfile(
        cpu_capacity=32,             # 32 cores (high-end server)
        memory_capacity=64.0,        # 64 GB RAM
        energy_cost_factor=0.7,      # Optimized efficiency
        sla_sensitivity=0.3,         # Flexible SLA (provider responsibility)
        communication_cost=4096,     # Large payload, premium bandwidth
        failure_probability=0.001,   # Extremely reliable
        max_workload=100.0           # Maximum capacity
    )
}


def get_node_profile(node_type: NodeType) -> NodeProfile:
    """
    Get profile for node type.
    
    Args:
        node_type: NodeType enum value
        
    Returns:
        NodeProfile instance for that type
        
    Raises:
        ValueError: If node_type not in NODE_PROFILES
    """
    if node_type not in NODE_PROFILES:
        raise ValueError(f"Unknown node type: {node_type}")
    return NODE_PROFILES[node_type]


def get_all_node_types() -> list:
    """Get list of all available node types."""
    return list(NodeType)


def get_node_type_by_name(name: str) -> NodeType:
    """
    Get node type by string name.
    
    Args:
        name: String name (e.g., "edge_device", "data_center_node")
        
    Returns:
        NodeType enum value
        
    Raises:
        ValueError: If name doesn't match any node type
    """
    for node_type in NodeType:
        if node_type.value == name.lower():
            return node_type
    raise ValueError(f"Unknown node type name: {name}")


# ============================================================================
# CONSTANTS: System-wide node behavior parameters
# ============================================================================

# Compute power model: CPU utilization impact on energy
CPU_POWER_COEFFICIENT = 0.6  # CPU accounts for 60% of energy variation

# Memory power model: Memory utilization impact on energy
MEMORY_POWER_COEFFICIENT = 0.4  # Memory accounts for 40% of energy variation

# Communication overhead: Bytes transmitted per federated round
# Total_comm = node.communication_cost * model_size_bytes
MODEL_SIZE_BYTES = 512  # Typical model size in bytes (very small for optimization)

# Workload generation bounds
MIN_WORKLOAD = 10.0
MAX_WORKLOAD = 100.0

# Resource utilization bounds
MIN_CPU_UTILIZATION = 5.0
MAX_CPU_UTILIZATION = 100.0

MIN_MEMORY_UTILIZATION = 5.0
MAX_MEMORY_UTILIZATION = 100.0

# Node lifecycle
DEFAULT_NODE_UPTIME_HOURS = 24
DEFAULT_NODE_DOWNTIME_PROBABILITY = 0.05  # Per round

# ============================================================================
# HETEROGENEITY METRICS
# ============================================================================

def compute_heterogeneity_index() -> Dict[str, float]:
    """
    Compute heterogeneity metrics across all node types.
    
    Useful for understanding ecosystem diversity.
    
    Returns:
        Dictionary with CPU, memory, energy heterogeneity indices
    """
    profiles = [NODE_PROFILES[nt] for nt in NodeType]
    
    cpu_values = [p.cpu_capacity for p in profiles]
    memory_values = [p.memory_capacity for p in profiles]
    energy_values = [p.energy_cost_factor for p in profiles]
    
    # Coefficient of variation as heterogeneity metric
    import numpy as np
    
    cpu_cv = np.std(cpu_values) / np.mean(cpu_values) if np.mean(cpu_values) > 0 else 0
    memory_cv = np.std(memory_values) / np.mean(memory_values) if np.mean(memory_values) > 0 else 0
    energy_cv = np.std(energy_values) / np.mean(energy_values) if np.mean(energy_values) > 0 else 0
    
    return {
        "cpu_heterogeneity": float(cpu_cv),
        "memory_heterogeneity": float(memory_cv),
        "energy_heterogeneity": float(energy_cv),
        "overall_heterogeneity": float((cpu_cv + memory_cv + energy_cv) / 3)
    }
