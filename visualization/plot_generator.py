"""
Plot Generator Module
Base utilities for creating research-grade visualizations.

Responsibility: Common plotting utilities, styling, color schemes.
"""

from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime


class PlotGenerator:
    """
    Base class for generating plots with consistent styling.
    
    Handles:
    - Color schemes and palettes
    - Plot styling and grid
    - Figure management
    - Export to PNG/PDF
    """
    
    # Consistent color palette for strategies
    STRATEGY_COLORS = {
        "static": "#1f77b4",           # Blue
        "centralized": "#ff7f0e",       # Orange
        "federated": "#2ca02c",         # Green
        "energy_aware": "#d62728",      # Red
    }
    
    # Node type colors
    NODE_TYPE_COLORS = {
        "edge_device": "#1f77b4",
        "user_device": "#ff7f0e",
        "compute_server": "#2ca02c",
        "data_center_node": "#d62728",
    }
    
    # Matplotlib style settings
    STYLE_SETTINGS = {
        "figure.figsize": (12, 7),
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "lines.linewidth": 2,
        "lines.markersize": 6,
    }
    
    @staticmethod
    def setup_style():
        """Configure matplotlib style for all plots."""
        plt.rcParams.update(PlotGenerator.STYLE_SETTINGS)
        plt.style.use("seaborn-v0_8-darkgrid")
    
    @staticmethod
    def get_strategy_color(strategy_name: str) -> str:
        """Get color for strategy."""
        return PlotGenerator.STRATEGY_COLORS.get(
            strategy_name.lower(), "#7f7f7f"
        )
    
    @staticmethod
    def get_node_type_color(node_type: str) -> str:
        """Get color for node type."""
        return PlotGenerator.NODE_TYPE_COLORS.get(
            node_type.lower(), "#7f7f7f"
        )
    
    @staticmethod
    def create_figure(title: str, figsize: Tuple[int, int] = (12, 7)):
        """Create a new figure with consistent styling."""
        PlotGenerator.setup_style()
        fig, ax = plt.subplots(figsize=figsize)
        fig.suptitle(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)
        return fig, ax
    
    @staticmethod
    def create_subplots(rows: int, cols: int, title: str = "",
                       figsize: Tuple[int, int] = (15, 10)):
        """Create subplot grid."""
        PlotGenerator.setup_style()
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        if title:
            fig.suptitle(title, fontsize=14, fontweight="bold")
        return fig, axes
    
    @staticmethod
    def add_legend(ax, strategy_names: List[str], loc: str = "best"):
        """Add legend with strategy colors."""
        patches = [
            mpatches.Patch(
                color=PlotGenerator.get_strategy_color(s),
                label=s.replace("_", " ").title()
            )
            for s in strategy_names
        ]
        ax.legend(handles=patches, loc=loc)
    
    @staticmethod
    def save_figure(fig, filename: str, dpi: int = 300):
        """Save figure to file."""
        fig.tight_layout()
        fig.savefig(filename, dpi=dpi, bbox_inches="tight")
        print(f"Figure saved: {filename}")
        plt.close(fig)
    
    @staticmethod
    def plot_line_series(ax, data: Dict[str, List[float]], 
                        x_label: str = "Rounds",
                        y_label: str = "Value",
                        title: str = ""):
        """Plot multiple line series."""
        for strategy_name, values in data.items():
            color = PlotGenerator.get_strategy_color(strategy_name)
            ax.plot(
                range(len(values)),
                values,
                label=strategy_name.replace("_", " ").title(),
                color=color,
                marker="o",
                linewidth=2,
                markersize=6
            )
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        if title:
            ax.set_title(title)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)
    
    @staticmethod
    def plot_bar_comparison(ax, data: Dict[str, float],
                           x_label: str = "",
                           y_label: str = "Value",
                           title: str = ""):
        """Plot bar chart for strategy comparison."""
        strategies = list(data.keys())
        values = list(data.values())
        colors = [PlotGenerator.get_strategy_color(s) for s in strategies]
        
        bars = ax.bar(
            [s.replace("_", " ").title() for s in strategies],
            values,
            color=colors,
            alpha=0.8,
            edgecolor="black",
            linewidth=1.5
        )
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f"{height:.2f}",
                ha="center",
                va="bottom",
                fontsize=10
            )
        
        ax.set_ylabel(y_label)
        if x_label:
            ax.set_xlabel(x_label)
        if title:
            ax.set_title(title)
        ax.grid(True, alpha=0.3, axis="y")
    
    @staticmethod
    def plot_heatmap(ax, data: np.ndarray, 
                    x_labels: List[str],
                    y_labels: List[str],
                    title: str = "",
                    cmap: str = "YlOrRd"):
        """Plot heatmap."""
        im = ax.imshow(data, cmap=cmap, aspect="auto")
        
        ax.set_xticks(range(len(x_labels)))
        ax.set_yticks(range(len(y_labels)))
        ax.set_xticklabels(x_labels, rotation=45, ha="right")
        ax.set_yticklabels(y_labels)
        
        # Add text annotations
        for i in range(len(y_labels)):
            for j in range(len(x_labels)):
                text = ax.text(
                    j, i, f"{data[i, j]:.1f}",
                    ha="center", va="center",
                    color="black", fontsize=9
                )
        
        if title:
            ax.set_title(title)
        
        plt.colorbar(im, ax=ax)
    
    @staticmethod
    def plot_pie_chart(ax, data: Dict[str, float], title: str = ""):
        """Plot pie chart for proportions."""
        labels = [k.replace("_", " ").title() for k in data.keys()]
        values = list(data.values())
        colors = [PlotGenerator.NODE_TYPE_COLORS.get(k, "#7f7f7f") 
                 for k in data.keys()]
        
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontsize": 10}
        )
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
        
        if title:
            ax.set_title(title)
    
    @staticmethod
    def plot_box_plot(ax, data: Dict[str, List[float]],
                     y_label: str = "Value",
                     title: str = ""):
        """Plot box plot for distribution comparison."""
        strategies = list(data.keys())
        values = [data[s] for s in strategies]
        
        bp = ax.boxplot(
            values,
            labels=[s.replace("_", " ").title() for s in strategies],
            patch_artist=True
        )
        
        # Color boxes
        for patch, strategy in zip(bp["boxes"], strategies):
            patch.set_facecolor(PlotGenerator.get_strategy_color(strategy))
            patch.set_alpha(0.7)
        
        ax.set_ylabel(y_label)
        if title:
            ax.set_title(title)
        ax.grid(True, alpha=0.3, axis="y")
    
    @staticmethod
    def plot_stacked_bar(ax, data: Dict[str, Dict[str, float]],
                        y_label: str = "Value",
                        title: str = ""):
        """Plot stacked bar chart."""
        categories = list(data.keys())
        
        # Get all subcategories
        subcats = set()
        for cat_data in data.values():
            subcats.update(cat_data.keys())
        subcats = sorted(list(subcats))
        
        # Prepare data
        x_pos = np.arange(len(categories))
        bottom = np.zeros(len(categories))
        
        colors = [PlotGenerator.NODE_TYPE_COLORS.get(sc, "#7f7f7f") 
                 for sc in subcats]
        
        for i, subcat in enumerate(subcats):
            values = [
                data[cat].get(subcat, 0) for cat in categories
            ]
            ax.bar(
                x_pos,
                values,
                bottom=bottom,
                label=subcat.replace("_", " ").title(),
                color=colors[i],
                alpha=0.8
            )
            bottom += np.array(values)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels([c.replace("_", " ").title() for c in categories])
        ax.set_ylabel(y_label)
        if title:
            ax.set_title(title)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3, axis="y")
