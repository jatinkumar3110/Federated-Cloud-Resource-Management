"""
Sustainability Metrics Module
Measures environmental impact of resource management strategies.

Research question: What is the carbon footprint and energy efficiency
of different resource management approaches?

Responsibility: Track energy consumption, carbon footprint, and
environmental sustainability metrics.
"""

from typing import List, Dict, Any, Optional
import numpy as np
from simulation.node import Node


class SustainabilityMetrics:
    """
    Analyzes environmental impact of federated resource management.
    
    Key metrics:
    - Total energy consumption (kWh)
    - Carbon footprint (kg CO2)
    - Power consumption (watts)
    - Energy efficiency (useful work per joule)
    - Green score (combined sustainability metric)
    
    Assumptions:
    - Energy in simulation = energy units (not physical watts)
    - Carbon intensity = 0.5 kg CO2 per kWh (varies by region)
    - Power efficiency = 0.8 (80% power delivery, 20% thermal loss)
    """
    
    # Regional carbon intensities (kg CO2 per kWh)
    CARBON_INTENSITIES = {
        "clean": 0.1,      # Renewable-heavy (e.g., Iceland)
        "mixed": 0.5,      # Grid average (global average ~0.5)
        "fossil": 0.9,     # Coal-heavy (e.g., Poland)
    }
    
    # PUE (Power Usage Effectiveness) by node type
    PUE_FACTORS = {
        "edge_device": 1.1,        # Mobile devices, less efficient
        "user_device": 1.15,       # User machines, variable cooling
        "compute_server": 1.2,     # Optimized but needs cooling
        "data_center_node": 1.05,  # Highly optimized facility
    }
    
    @staticmethod
    def compute_total_energy_kwh(nodes: List[Node]) -> float:
        """
        Compute total energy consumed by all nodes (in kWh).
        
        Args:
            nodes: List of nodes to analyze
            
        Returns:
            float: Total energy in kilowatt-hours
        """
        total_energy_units = sum(node.energy_consumed for node in nodes)
        
        # Convert simulation units to kWh
        # Assumption: 1 energy unit ≈ 0.001 kWh
        kwh = total_energy_units * 0.001
        
        return float(kwh)
    
    @staticmethod
    def compute_carbon_footprint(nodes: List[Node], 
                                region: str = "mixed") -> float:
        """
        Compute carbon footprint of simulation.
        
        Args:
            nodes: List of nodes
            region: Regional carbon intensity ("clean", "mixed", "fossil")
            
        Returns:
            float: Carbon footprint in kg CO2
        """
        if region not in SustainabilityMetrics.CARBON_INTENSITIES:
            region = "mixed"
        
        carbon_intensity = SustainabilityMetrics.CARBON_INTENSITIES[region]
        total_kwh = SustainabilityMetrics.compute_total_energy_kwh(nodes)
        
        carbon_kg = total_kwh * carbon_intensity
        return float(carbon_kg)
    
    @staticmethod
    def compute_average_power(nodes: List[Node], duration_seconds: float) -> float:
        """
        Estimate average power consumption during simulation.
        
        Args:
            nodes: List of nodes
            duration_seconds: Total duration
            
        Returns:
            float: Average power in watts
        """
        if duration_seconds == 0:
            return 0.0
        
        total_kwh = SustainabilityMetrics.compute_total_energy_kwh(nodes)
        total_joules = total_kwh * 3.6e6  # 1 kWh = 3.6 million joules
        
        average_watts = total_joules / duration_seconds
        return float(average_watts)
    
    @staticmethod
    def compute_energy_efficiency(nodes: List[Node], 
                                 useful_work: float = 1.0) -> float:
        """
        Compute energy efficiency ratio (useful work per joule).
        
        Args:
            nodes: List of nodes
            useful_work: Amount of useful computation (normalized to [0, 1])
            
        Returns:
            float: Efficiency in work units per joule
        """
        total_kwh = SustainabilityMetrics.compute_total_energy_kwh(nodes)
        
        if total_kwh == 0:
            return 0.0
        
        total_joules = total_kwh * 3.6e6
        efficiency = useful_work / total_joules
        
        return float(efficiency)
    
    @staticmethod
    def compute_pue_overhead(nodes: List[Node]) -> float:
        """
        Compute Power Usage Effectiveness overhead.
        
        PUE = Total facility power / IT equipment power
        PUE > 1.0 accounts for cooling, power conversion losses.
        
        Args:
            nodes: List of nodes
            
        Returns:
            float: Average PUE across nodes
        """
        if len(nodes) == 0:
            return 1.0
        
        pue_values = []
        for node in nodes:
            node_type = node.node_type.name
            if node_type in SustainabilityMetrics.PUE_FACTORS:
                pue = SustainabilityMetrics.PUE_FACTORS[node_type]
            else:
                pue = 1.15  # Default
            pue_values.append(pue)
        
        return float(np.mean(pue_values))
    
    @staticmethod
    def compute_green_score(nodes: List[Node], 
                           region: str = "mixed",
                           target_carbon_kg: float = 10.0) -> float:
        """
        Compute overall green score (normalized sustainability).
        
        Green score combines:
        - Carbon efficiency: how much work per kg CO2
        - Energy efficiency: how much work per joule
        - Green intensity: carbon per useful work unit
        
        Score: [0, 1] where 1 = very sustainable, 0 = unsustainable
        
        Args:
            nodes: List of nodes
            region: Carbon intensity region
            target_carbon_kg: Target carbon budget
            
        Returns:
            float: Green score in [0, 1]
        """
        carbon = SustainabilityMetrics.compute_carbon_footprint(
            nodes, region
        )
        
        if carbon == 0:
            return 1.0
        
        # Compare to target: lower is better
        carbon_efficiency = max(0, 1.0 - (carbon / target_carbon_kg))
        
        # Energy efficiency component
        energy_kwh = SustainabilityMetrics.compute_total_energy_kwh(nodes)
        
        if energy_kwh > 100:  # High energy consumption
            energy_score = 0.3
        elif energy_kwh > 50:
            energy_score = 0.6
        elif energy_kwh > 10:
            energy_score = 0.8
        else:
            energy_score = 1.0
        
        # Combined score (weighted average)
        green_score = 0.6 * carbon_efficiency + 0.4 * energy_score
        
        return float(np.clip(green_score, 0.0, 1.0))
    
    @staticmethod
    def compute_energy_breakdown(nodes: List[Node]) -> Dict[str, float]:
        """
        Breakdown energy consumption by node type.
        
        Args:
            nodes: List of nodes
            
        Returns:
            Dictionary: energy by node type
        """
        breakdown = {}
        
        for node in nodes:
            node_type = node.node_type.name
            energy = node.energy_consumed
            
            if node_type not in breakdown:
                breakdown[node_type] = 0.0
            
            breakdown[node_type] += energy
        
        # Convert to percentages
        total = sum(breakdown.values())
        if total > 0:
            breakdown = {k: (v / total * 100) for k, v in breakdown.items()}
        
        return breakdown
    
    @staticmethod
    def compute_per_node_efficiency(node: Node, 
                                   useful_work: float = 1.0) -> float:
        """
        Compute energy efficiency for single node.
        
        Args:
            node: Node to analyze
            useful_work: Amount of useful work done
            
        Returns:
            float: Work units per kWh
        """
        kwh = node.energy_consumed * 0.001
        
        if kwh == 0:
            return 0.0
        
        efficiency = useful_work / kwh
        return float(efficiency)
    
    @staticmethod
    def get_sustainability_summary(nodes: List[Node],
                                  duration_seconds: float = 3600,
                                  region: str = "mixed") -> Dict[str, Any]:
        """
        Get comprehensive sustainability analysis.
        
        Args:
            nodes: List of nodes
            duration_seconds: Total duration of simulation
            region: Carbon intensity region
            
        Returns:
            Dictionary with all sustainability metrics
        """
        energy_kwh = SustainabilityMetrics.compute_total_energy_kwh(nodes)
        carbon_kg = SustainabilityMetrics.compute_carbon_footprint(
            nodes, region
        )
        
        return {
            "total_energy_kwh": energy_kwh,
            "carbon_footprint_kg": carbon_kg,
            "average_power_watts": SustainabilityMetrics.compute_average_power(
                nodes, duration_seconds
            ),
            "energy_efficiency": SustainabilityMetrics.compute_energy_efficiency(
                nodes, useful_work=1.0
            ),
            "pue_overhead": SustainabilityMetrics.compute_pue_overhead(nodes),
            "green_score": SustainabilityMetrics.compute_green_score(
                nodes, region
            ),
            "energy_breakdown_percent": SustainabilityMetrics.compute_energy_breakdown(
                nodes
            ),
            "carbon_intensity": SustainabilityMetrics.CARBON_INTENSITIES.get(
                region, SustainabilityMetrics.CARBON_INTENSITIES["mixed"]
            ),
        }
