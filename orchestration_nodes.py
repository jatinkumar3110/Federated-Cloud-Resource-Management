"""
Interactive Node Configuration Manager

Manages user-defined cloud nodes for interactive simulation playground.
Stores node configurations in memory and converts them to Node objects for simulation.

Do NOT include simulation or metrics logic - UI/API layer only.
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from simulation.node_types import NodeType
from simulation.node import Node


@dataclass
class NodeConfig:
    """User-defined node configuration."""
    node_id: str
    node_type: str
    cpu_cores: int
    memory_gb: float
    energy_cost_factor: float
    sla_threshold: float
    region: str
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    @staticmethod
    def from_dict(data: dict) -> 'NodeConfig':
        """Create from dictionary."""
        return NodeConfig(**data)


class NodesManager:
    """
    Manages in-memory node configurations.
    
    Responsibilities:
    - Store/retrieve/update/delete node configurations
    - Validate node inputs
    - Convert UI inputs to Node objects for simulation
    - Support session-based persistence
    """
    
    def __init__(self):
        """Initialize with empty node store."""
        self.nodes: Dict[str, NodeConfig] = {}
        self.next_id = 1
    
    def add_node(self, node_type: str, cpu_cores: int, memory_gb: float,
                 energy_cost_factor: float, sla_threshold: float,
                 region: str = "mixed") -> NodeConfig:
        """
        Add a new node configuration.
        
        Args:
            node_type: EDGE_DEVICE, USER_DEVICE, COMPUTE_SERVER, or DATA_CENTER_NODE
            cpu_cores: Number of CPU cores (int > 0)
            memory_gb: Memory in GB (float > 0)
            energy_cost_factor: Energy multiplier (float > 0)
            sla_threshold: SLA target percentage (0-100)
            region: "clean", "mixed", or "fossil"
        
        Returns:
            NodeConfig object
        
        Raises:
            ValueError: If inputs are invalid
        """
        # Validate node type
        valid_types = {
            "EDGE_DEVICE", "USER_DEVICE", "COMPUTE_SERVER", "DATA_CENTER_NODE",
            "edge_device", "user_device", "compute_server", "data_center_node"
        }
        if node_type not in valid_types:
            raise ValueError(f"Invalid node type: {node_type}. Must be one of {valid_types}")
        
        # Normalize node type to uppercase
        node_type = node_type.upper() if "_" in node_type else node_type
        
        # Validate numeric inputs
        if cpu_cores <= 0:
            raise ValueError("CPU cores must be > 0")
        if memory_gb <= 0:
            raise ValueError("Memory must be > 0")
        if energy_cost_factor <= 0:
            raise ValueError("Energy cost factor must be > 0")
        if not (0 <= sla_threshold <= 100):
            raise ValueError("SLA threshold must be between 0 and 100")
        
        # Validate region
        valid_regions = {"clean", "mixed", "fossil"}
        if region not in valid_regions:
            raise ValueError(f"Invalid region: {region}. Must be one of {valid_regions}")
        
        # Generate unique node ID
        node_id = f"node_{self.next_id}"
        self.next_id += 1
        
        # Create configuration
        config = NodeConfig(
            node_id=node_id,
            node_type=node_type,
            cpu_cores=cpu_cores,
            memory_gb=memory_gb,
            energy_cost_factor=energy_cost_factor,
            sla_threshold=sla_threshold,
            region=region
        )
        
        self.nodes[node_id] = config
        return config
    
    def get_node(self, node_id: str) -> Optional[NodeConfig]:
        """Get node configuration by ID."""
        return self.nodes.get(node_id)
    
    def get_all_nodes(self) -> List[NodeConfig]:
        """Get all node configurations."""
        return list(self.nodes.values())
    
    def update_node(self, node_id: str, **kwargs) -> NodeConfig:
        """
        Update node configuration.
        
        Args:
            node_id: Node ID to update
            **kwargs: Fields to update (node_type, cpu_cores, memory_gb, etc.)
        
        Returns:
            Updated NodeConfig
        
        Raises:
            KeyError: If node_id not found
            ValueError: If inputs are invalid
        """
        if node_id not in self.nodes:
            raise KeyError(f"Node {node_id} not found")
        
        config = self.nodes[node_id]
        
        # Update fields with validation
        if 'node_type' in kwargs:
            valid_types = {"EDGE_DEVICE", "USER_DEVICE", "COMPUTE_SERVER", "DATA_CENTER_NODE"}
            if kwargs['node_type'] not in valid_types:
                raise ValueError(f"Invalid node type: {kwargs['node_type']}")
            config.node_type = kwargs['node_type']
        
        if 'cpu_cores' in kwargs:
            if kwargs['cpu_cores'] <= 0:
                raise ValueError("CPU cores must be > 0")
            config.cpu_cores = kwargs['cpu_cores']
        
        if 'memory_gb' in kwargs:
            if kwargs['memory_gb'] <= 0:
                raise ValueError("Memory must be > 0")
            config.memory_gb = kwargs['memory_gb']
        
        if 'energy_cost_factor' in kwargs:
            if kwargs['energy_cost_factor'] <= 0:
                raise ValueError("Energy cost factor must be > 0")
            config.energy_cost_factor = kwargs['energy_cost_factor']
        
        if 'sla_threshold' in kwargs:
            if not (0 <= kwargs['sla_threshold'] <= 100):
                raise ValueError("SLA threshold must be between 0 and 100")
            config.sla_threshold = kwargs['sla_threshold']
        
        if 'region' in kwargs:
            valid_regions = {"clean", "mixed", "fossil"}
            if kwargs['region'] not in valid_regions:
                raise ValueError(f"Invalid region: {kwargs['region']}")
            config.region = kwargs['region']
        
        return config
    
    def delete_node(self, node_id: str) -> bool:
        """
        Delete node configuration.
        
        Args:
            node_id: Node ID to delete
        
        Returns:
            True if deleted, False if not found
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            return True
        return False
    
    def clear_all(self):
        """Clear all nodes."""
        self.nodes.clear()
    
    def to_nodes(self) -> List[Node]:
        """
        Convert all configurations to Node objects for simulation.
        
        Returns:
            List of Node objects with user-defined parameters
        
        Note: Node objects use NodeProfile which is determined by NodeType.
        Custom CPU/memory parameters are stored in the config but used
        as reference - actual Node class uses NodeType profiles.
        """
        nodes = []
        node_id = 0
        
        for config in self.nodes.values():
            # Map string node type to NodeType enum
            node_type_map = {
                "EDGE_DEVICE": NodeType.EDGE_DEVICE,
                "USER_DEVICE": NodeType.USER_DEVICE,
                "COMPUTE_SERVER": NodeType.COMPUTE_SERVER,
                "DATA_CENTER_NODE": NodeType.DATA_CENTER_NODE,
            }
            
            node_type = node_type_map.get(config.node_type, NodeType.USER_DEVICE)
            
            # Create Node object (uses NodeType profile)
            node = Node(
                node_id=node_id,
                node_type=node_type,
                random_seed=42
            )
            
            # Store user configuration as metadata for reference
            # This allows tracking what user requested vs what profile provides
            node._user_config = config
            
            nodes.append(node)
            node_id += 1
        
        return nodes
    
    def to_dict(self) -> Dict:
        """Export all nodes as dictionary for JSON serialization."""
        return {
            "nodes": [config.to_dict() for config in self.nodes.values()],
            "count": len(self.nodes)
        }
    
    def from_dict(self, data: Dict):
        """Import nodes from dictionary."""
        self.clear_all()
        for node_data in data.get("nodes", []):
            config = NodeConfig.from_dict(node_data)
            self.nodes[config.node_id] = config
            # Update next_id to avoid collisions
            if config.node_id.startswith("node_"):
                try:
                    node_num = int(config.node_id.split("_")[1])
                    self.next_id = max(self.next_id, node_num + 1)
                except (ValueError, IndexError):
                    pass


# Global instance for session management
_global_nodes_manager = NodesManager()


def get_nodes_manager() -> NodesManager:
    """Get global nodes manager instance."""
    return _global_nodes_manager
