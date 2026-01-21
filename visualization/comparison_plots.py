"""
Comparison Plots Module
Generates strategy comparison visualizations.

Responsibility: Create comparative plots for research analysis.
Called by: experiments, dashboard
"""

from typing import Dict, List, Any, Optional
import numpy as np
import matplotlib.pyplot as plt

from visualization.plot_generator import PlotGenerator
from simulation.node import Node
from metrics.fairness import FairnessMetrics
from metrics.communication import CommunicationMetrics
from metrics.sustainability import SustainabilityMetrics


class ComparisonPlots:
    """
    Generates comparative plots showing strategy performance.
    
    Plots:
    - Energy consumption over time
    - SLA violations trend
    - Fairness metrics comparison
    - Communication overhead
    - Carbon footprint comparison
    - Node utilization heatmap
    - Strategy radar chart
    """
    
    @staticmethod
    def plot_energy_comparison(energy_per_round: Dict[str, List[float]],
                              filename: str = "energy_comparison.png"):
        """
        Plot energy consumption per round for all strategies.
        
        Args:
            energy_per_round: Dict mapping strategy to list of energies
            filename: Output filename
        """
        fig, ax = PlotGenerator.create_figure(
            "Energy Consumption Over Rounds"
        )
        
        PlotGenerator.plot_line_series(
            ax,
            energy_per_round,
            x_label="Round",
            y_label="Energy Units",
            title=""
        )
        
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_sla_violations(sla_per_round: Dict[str, List[int]],
                           filename: str = "sla_violations.png"):
        """
        Plot cumulative SLA violations.
        
        Args:
            sla_per_round: Dict mapping strategy to list of violation counts
            filename: Output filename
        """
        fig, ax = PlotGenerator.create_figure(
            "SLA Violations Trend"
        )
        
        # Convert to cumulative
        cumulative_sla = {}
        for strategy, sla_list in sla_per_round.items():
            cumulative_sla[strategy] = np.cumsum(sla_list).tolist()
        
        PlotGenerator.plot_line_series(
            ax,
            cumulative_sla,
            x_label="Round",
            y_label="Cumulative Violations",
            title=""
        )
        
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_fairness_comparison(fairness_scores: Dict[str, float],
                                filename: str = "fairness_comparison.png"):
        """
        Plot fairness metrics comparison.
        
        Args:
            fairness_scores: Dict mapping strategy to fairness score [0,1]
            filename: Output filename
        """
        fig, ax = PlotGenerator.create_figure(
            "Fairness Metrics Comparison"
        )
        
        PlotGenerator.plot_bar_comparison(
            ax,
            fairness_scores,
            y_label="Fairness Score [0-1]",
            title=""
        )
        
        # Add reference line for perfect fairness
        ax.axhline(y=1.0, color="green", linestyle="--", 
                  linewidth=2, label="Perfect Fairness")
        ax.set_ylim([0, 1.1])
        ax.legend()
        
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_communication_overhead(comm_bytes: Dict[str, float],
                                   filename: str = "communication_overhead.png"):
        """
        Plot communication overhead comparison.
        
        Args:
            comm_bytes: Dict mapping strategy to total bytes
            filename: Output filename
        """
        fig, ax = PlotGenerator.create_figure(
            "Communication Overhead"
        )
        
        # Convert to MB for readability
        comm_mb = {k: v / (1024*1024) for k, v in comm_bytes.items()}
        
        PlotGenerator.plot_bar_comparison(
            ax,
            comm_mb,
            y_label="Total Bytes (MB)",
            title=""
        )
        
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_carbon_footprint(carbon_kg: Dict[str, Dict[str, float]],
                             filename: str = "carbon_footprint.png"):
        """
        Plot carbon footprint by region.
        
        Args:
            carbon_kg: Dict[strategy][region] -> kg CO2
            filename: Output filename
        """
        fig, ax = PlotGenerator.create_figure(
            "Carbon Footprint by Region"
        )
        
        # Prepare data for stacked bar
        regions = ["clean", "mixed", "fossil"]
        strategies = list(carbon_kg.keys())
        
        x_pos = np.arange(len(strategies))
        bottom = np.zeros(len(strategies))
        
        colors = {
            "clean": "#2ca02c",
            "mixed": "#ff7f0e",
            "fossil": "#d62728"
        }
        
        for region in regions:
            values = [carbon_kg.get(s, {}).get(region, 0) for s in strategies]
            ax.bar(
                x_pos,
                values,
                bottom=bottom,
                label=region.title(),
                color=colors.get(region, "#7f7f7f"),
                alpha=0.8
            )
            bottom += np.array(values)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels([s.replace("_", " ").title() for s in strategies])
        ax.set_ylabel("Carbon Emissions (kg CO2)")
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3, axis="y")
        
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_node_utilization_heatmap(utilization: Dict[str, List[float]],
                                     round_numbers: List[int] = None,
                                     filename: str = "node_utilization.png"):
        """
        Plot node utilization heatmap over rounds.
        
        Args:
            utilization: Dict[node_id] -> list of utilization values
            round_numbers: Round numbers (optional)
            filename: Output filename
        """
        fig, ax = PlotGenerator.create_figure(
            "Node Utilization Heatmap",
            figsize=(12, 6)
        )
        
        # Prepare data
        nodes = list(utilization.keys())
        num_rounds = max(len(vals) for vals in utilization.values())
        
        # Pad data to uniform length
        data = np.zeros((len(nodes), num_rounds))
        for i, node_id in enumerate(nodes):
            data[i, :len(utilization[node_id])] = utilization[node_id]
        
        x_labels = round_numbers or list(range(num_rounds))
        
        PlotGenerator.plot_heatmap(
            ax,
            data,
            x_labels=[f"R{r}" for r in x_labels],
            y_labels=nodes,
            title="",
            cmap="YlOrRd"
        )
        
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_node_contribution(contributions: Dict[str, float],
                              filename: str = "node_contribution.png"):
        """
        Plot pie chart of node contributions.
        
        Args:
            contributions: Dict[node_type] -> contribution value
            filename: Output filename
        """
        fig, ax = PlotGenerator.create_figure(
            "Node Type Contribution"
        )
        
        PlotGenerator.plot_pie_chart(ax, contributions, title="")
        
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_strategy_comparison_dashboard(
        strategies_data: Dict[str, Dict[str, Any]],
        filename_prefix: str = "comparison"
    ):
        """
        Create comprehensive strategy comparison dashboard.
        
        Args:
            strategies_data: Dict[strategy] -> Dict[metric] -> value
            filename_prefix: Prefix for output files
        """
        fig, axes = PlotGenerator.create_subplots(
            2, 2,
            title="Strategy Comparison Dashboard",
            figsize=(16, 12)
        )
        axes = axes.flatten()
        
        # Extract data
        strategies = list(strategies_data.keys())
        
        # Plot 1: Energy vs Fairness (scatter)
        energy_vals = []
        fairness_vals = []
        for s in strategies:
            energy_vals.append(strategies_data[s].get("total_energy", 0))
            fairness_vals.append(strategies_data[s].get("fairness", 0.5))
        
        for i, strategy in enumerate(strategies):
            color = PlotGenerator.get_strategy_color(strategy)
            axes[0].scatter(
                energy_vals[i],
                fairness_vals[i],
                s=300,
                color=color,
                label=strategy.replace("_", " ").title(),
                alpha=0.7,
                edgecolors="black",
                linewidth=2
            )
        
        axes[0].set_xlabel("Total Energy (units)")
        axes[0].set_ylabel("Fairness Score [0-1]")
        axes[0].set_title("Energy vs Fairness Trade-off")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: SLA violations
        sla_vals = {s: strategies_data[s].get("sla_violations", 0) 
                   for s in strategies}
        PlotGenerator.plot_bar_comparison(
            axes[1],
            sla_vals,
            y_label="Total SLA Violations",
            title="SLA Performance"
        )
        
        # Plot 3: Communication overhead
        comm_vals = {s: strategies_data[s].get("communication_bytes", 0) / (1024*1024)
                    for s in strategies}
        PlotGenerator.plot_bar_comparison(
            axes[2],
            comm_vals,
            y_label="Communication (MB)",
            title="Communication Overhead"
        )
        
        # Plot 4: Green score
        green_vals = {s: strategies_data[s].get("green_score", 0.5)
                     for s in strategies}
        PlotGenerator.plot_bar_comparison(
            axes[3],
            green_vals,
            y_label="Green Score [0-1]",
            title="Sustainability"
        )
        axes[3].set_ylim([0, 1.1])
        
        # Save figure
        filename = f"{filename_prefix}_dashboard.png"
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_convergence_curves(
        loss_history: Dict[str, List[float]],
        filename: str = "convergence_curves.png"
    ):
        """
        Plot model training convergence curves.
        
        Args:
            loss_history: Dict[strategy] -> list of loss values
            filename: Output filename
        """
        fig, ax = PlotGenerator.create_figure(
            "Model Convergence Curves"
        )
        
        PlotGenerator.plot_line_series(
            ax,
            loss_history,
            x_label="Training Step",
            y_label="Loss",
            title=""
        )
        
        PlotGenerator.save_figure(fig, filename)
    
    @staticmethod
    def plot_allocation_distribution(
        allocation_stats: Dict[str, Dict[str, float]],
        filename: str = "allocation_distribution.png"
    ):
        """
        Plot resource allocation distribution by node type.
        
        Args:
            allocation_stats: Dict[strategy][node_type] -> avg allocation %
            filename: Output filename
        """
        fig, axes = PlotGenerator.create_subplots(
            1, len(allocation_stats),
            figsize=(5 * len(allocation_stats), 5)
        )
        
        if len(allocation_stats) == 1:
            axes = [axes]
        
        for idx, (strategy, node_allocs) in enumerate(allocation_stats.items()):
            PlotGenerator.plot_pie_chart(
                axes[idx],
                node_allocs,
                title=strategy.replace("_", " ").title()
            )
        
        fig.suptitle("Resource Allocation Distribution by Node Type", 
                    fontsize=14, fontweight="bold")
        PlotGenerator.save_figure(fig, filename)
