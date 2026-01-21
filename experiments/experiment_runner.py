"""
Experiment Runner Module
Executes batch experiments and aggregates results.

Responsibility: Run experiments, collect metrics, aggregate results.
Called by: dashboard, orchestration
"""

from typing import Dict, List, Any, Tuple
import numpy as np
import csv
from datetime import datetime

from experiments.scenario_manager import Scenario
from simulation.node import Node
from simulation.node_types import NodeType
from ui.dashboard_controller import DashboardController
from metrics.fairness import FairnessMetrics
from metrics.communication import CommunicationMetrics
from metrics.sustainability import SustainabilityMetrics


class ExperimentRunner:
    """
    Runs experiments and collects results.
    
    Workflow:
    1. Load scenario (nodes, strategies, parameters)
    2. For each strategy:
       - Create nodes
       - Initialize strategy
       - Run federated rounds
       - Collect metrics
    3. Aggregate results
    4. Export to CSV
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize experiment runner.
        
        Args:
            verbose: Print progress information
        """
        self.verbose = verbose
        self.results = {}
        self.controller = DashboardController()
    
    def run_experiment(
        self,
        scenario: Scenario,
        output_file: str = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Run a single experiment scenario.
        
        Args:
            scenario: Experiment scenario
            output_file: Optional CSV file to save results
            
        Returns:
            Dict[strategy] -> Dict[metric] -> value
        """
        if self.verbose:
            print(f"\n{'=' * 60}")
            print(f"Experiment: {scenario.name}")
            print(f"Description: {scenario.description}")
            print(f"Rounds: {scenario.num_rounds}")
            print(f"Strategies: {', '.join(scenario.strategies)}")
            print(f"{'=' * 60}")
        
        results = {}
        
        for strategy_name in scenario.strategies:
            if self.verbose:
                print(f"\nRunning: {strategy_name}")
            
            # Create nodes from scenario specification
            nodes = []
            node_id = 0
            
            for node_type_name, count in scenario.num_nodes_per_type.items():
                # Map string name to NodeType enum
                node_type = NodeType[node_type_name.upper()]
                for _ in range(count):
                    node = Node(node_id, node_type, random_seed=42 + node_id)
                    nodes.append(node)
                    node_id += 1
            
            # Create strategy
            strategy = self.controller.create_strategy(
                strategy_name,
                alpha=scenario.alpha,
                beta=scenario.beta,
                gamma=scenario.gamma,
            )
            
            # Run experiment
            strategy_results = self._run_strategy(
                strategy,
                nodes,
                scenario.num_rounds,
                strategy_name,
            )
            
            results[strategy_name] = strategy_results
        
        self.results = results
        
        # Export results
        if output_file:
            self.export_results_csv(results, output_file, scenario)
        
        if self.verbose:
            self._print_summary(results)
        
        return results
    
    def _run_strategy(
        self,
        strategy,
        nodes: List,
        num_rounds: int,
        strategy_name: str,
    ) -> Dict[str, Any]:
        """
        Run single strategy with nodes.
        
        Args:
            strategy: Strategy instance
            nodes: List of nodes
            num_rounds: Number of federated rounds
            strategy_name: Strategy identifier
            
        Returns:
            Dictionary of metrics
        """
        # Run federated rounds
        energy_history = []
        sla_history = []
        
        for round_num in range(num_rounds):
            # Allocate resources using strategy
            allocation = strategy.execute_allocation(nodes)
            
            # Simulate computation
            for node in nodes:
                node.generate_workload()
                
                if allocation.get(node.node_id):
                    cpu_pct = allocation[node.node_id].get("cpu_percent", 50)
                    mem_pct = allocation[node.node_id].get("memory_percent", 50)
                    node.allocate_resources(cpu_pct, mem_pct)
                
                # Compute energy
                node.compute_energy_consumption(duration_seconds=10)
            
            # Track metrics
            total_energy = sum(n.energy_consumed for n in nodes)
            total_sla = sum(n.sla_violations for n in nodes)
            
            energy_history.append(total_energy)
            sla_history.append(total_sla)
        
        # Compute aggregate metrics
        return {
            "total_energy": float(np.sum(energy_history)),
            "avg_energy": float(np.mean(energy_history)),
            "energy_std": float(np.std(energy_history)),
            "total_sla_violations": int(np.sum(sla_history)),
            "fairness_score": FairnessMetrics.compute_fairness_score(nodes),
            "communication_bytes": CommunicationMetrics.compute_total_overhead(
                nodes, num_rounds, model_size_bytes=512
            ),
            "green_score": SustainabilityMetrics.compute_green_score(
                nodes, region="mixed"
            ),
            "energy_history": energy_history,
            "sla_history": sla_history,
        }
    
    def _print_summary(self, results: Dict[str, Dict[str, Any]]):
        """Print summary of experiment results."""
        print(f"\n{'=' * 60}")
        print("EXPERIMENT RESULTS SUMMARY")
        print(f"{'=' * 60}\n")
        
        for strategy, metrics in results.items():
            print(f"{strategy.upper()}:")
            print(f"  Total Energy: {metrics['total_energy']:.3f} units")
            print(f"  Avg Energy: {metrics['avg_energy']:.3f} units")
            print(f"  SLA Violations: {metrics['total_sla_violations']}")
            print(f"  Fairness: {metrics['fairness_score']:.3f}")
            print(f"  Green Score: {metrics['green_score']:.3f}")
            print()
    
    def export_results_csv(
        self,
        results: Dict[str, Dict[str, Any]],
        filepath: str,
        scenario: Scenario = None,
    ):
        """
        Export results to CSV file.
        
        Args:
            results: Results dictionary
            filepath: Output CSV path
            scenario: Optional scenario info
        """
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            if scenario:
                writer.writerow(["Experiment", scenario.name])
                writer.writerow(["Timestamp", datetime.now().isoformat()])
                writer.writerow([])
            
            # Results table
            writer.writerow([
                "Strategy",
                "Total Energy",
                "Avg Energy",
                "Energy Std",
                "SLA Violations",
                "Fairness",
                "Communication (MB)",
                "Green Score",
            ])
            
            for strategy, metrics in results.items():
                writer.writerow([
                    strategy,
                    f"{metrics['total_energy']:.3f}",
                    f"{metrics['avg_energy']:.3f}",
                    f"{metrics['energy_std']:.3f}",
                    metrics['total_sla_violations'],
                    f"{metrics['fairness_score']:.3f}",
                    f"{metrics['communication_bytes'] / (1024*1024):.2f}",
                    f"{metrics['green_score']:.3f}",
                ])
        
        print(f"Results exported: {filepath}")
    
    def run_batch(
        self,
        scenarios: List[Scenario],
        output_dir: str = "experiment_results",
    ) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Run multiple experiment scenarios.
        
        Args:
            scenarios: List of scenarios
            output_dir: Output directory for CSV files
            
        Returns:
            Dict[scenario_name][strategy] -> metrics
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        all_results = {}
        
        for scenario in scenarios:
            csv_file = f"{output_dir}/{scenario.name.lower().replace(' ', '_')}.csv"
            
            results = self.run_experiment(scenario, output_file=csv_file)
            all_results[scenario.name] = results
        
        return all_results
    
    def compare_strategies(
        self,
        scenario: Scenario,
    ) -> Dict[str, float]:
        """
        Compare strategy performance using multiple metrics.
        
        Args:
            scenario: Experiment scenario
            
        Returns:
            Dict with comparative analysis
        """
        results = self.run_experiment(scenario)
        
        # Normalize metrics to [0, 1] for comparison
        metrics_names = ["total_energy", "fairness_score", "green_score"]
        
        comparison = {}
        for metric in metrics_names:
            values = [r.get(metric, 0) for r in results.values()]
            
            min_val = min(values) if values else 0
            max_val = max(values) if values else 1
            
            normalized = {}
            for strategy, res in results.items():
                if max_val > min_val:
                    norm_val = (res[metric] - min_val) / (max_val - min_val)
                else:
                    norm_val = 0
                normalized[strategy] = norm_val
            
            comparison[metric] = normalized
        
        return comparison
    
    @staticmethod
    def aggregate_results(
        all_results: Dict[str, Dict[str, Dict[str, Any]]],
    ) -> Dict[str, Dict[str, float]]:
        """
        Aggregate results across multiple experiments.
        
        Args:
            all_results: Results from multiple scenarios
            
        Returns:
            Aggregated metrics by strategy
        """
        strategy_stats = {}
        
        for scenario_name, scenario_results in all_results.items():
            for strategy, metrics in scenario_results.items():
                if strategy not in strategy_stats:
                    strategy_stats[strategy] = {
                        "energy": [],
                        "sla": [],
                        "fairness": [],
                        "green": [],
                    }
                
                strategy_stats[strategy]["energy"].append(metrics["total_energy"])
                strategy_stats[strategy]["sla"].append(metrics["total_sla_violations"])
                strategy_stats[strategy]["fairness"].append(metrics["fairness_score"])
                strategy_stats[strategy]["green"].append(metrics["green_score"])
        
        # Compute aggregate statistics
        aggregated = {}
        for strategy, stats in strategy_stats.items():
            aggregated[strategy] = {
                "avg_energy": float(np.mean(stats["energy"])),
                "std_energy": float(np.std(stats["energy"])),
                "total_sla": int(np.sum(stats["sla"])),
                "avg_fairness": float(np.mean(stats["fairness"])),
                "avg_green": float(np.mean(stats["green"])),
            }
        
        return aggregated
