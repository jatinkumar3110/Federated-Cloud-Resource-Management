"""
Generate documentation images for Federated Cloud Dashboard project.
Creates visualizations for: Dashboard, System Architecture, Proposed Methodology, and Experimental Setup.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# Create output directory
output_dir = os.path.join(os.path.dirname(__file__), 'documentation_images')
os.makedirs(output_dir, exist_ok=True)

# Color scheme
COLOR_PRIMARY = '#2563EB'      # Blue
COLOR_SECONDARY = '#7C3AED'    # Purple
COLOR_SUCCESS = '#16A34A'      # Green
COLOR_WARNING = '#EA580C'      # Orange
COLOR_LIGHT = '#F3F4F6'        # Light gray
COLOR_TEXT = '#1F2937'         # Dark gray

# ============================================================================
# 1. DASHBOARD IMAGE
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Header
header_box = FancyBboxPatch((0.2, 8.5), 9.6, 1.2, boxstyle="round,pad=0.1", 
                            edgecolor=COLOR_PRIMARY, facecolor=COLOR_PRIMARY, 
                            linewidth=2, alpha=0.9)
ax.add_patch(header_box)
ax.text(5, 9.1, 'Federated Cloud Dashboard', ha='center', va='center', 
        fontsize=18, fontweight='bold', color='white')

# Navigation tabs
tabs = ['Overview', 'Simulations', 'Experiments', 'Analytics']
tab_x = 0.5
for i, tab in enumerate(tabs):
    tab_box = FancyBboxPatch((tab_x + i*2.3, 7.9), 2.1, 0.5, 
                             boxstyle="round,pad=0.05",
                             edgecolor=COLOR_TEXT if i == 0 else '#D1D5DB',
                             facecolor=COLOR_PRIMARY if i == 0 else COLOR_LIGHT,
                             linewidth=1.5, alpha=0.8)
    ax.add_patch(tab_box)
    ax.text(tab_x + i*2.3 + 1.05, 8.16, tab, ha='center', va='center',
            fontsize=10, fontweight='bold', color='white' if i == 0 else COLOR_TEXT)

# Left Sidebar
sidebar_box = FancyBboxPatch((0.2, 0.5), 2, 7.2, boxstyle="round,pad=0.05",
                            edgecolor='#E5E7EB', facecolor=COLOR_LIGHT,
                            linewidth=1.5)
ax.add_patch(sidebar_box)

sidebar_items = ['Run Simulation', 'Execute Experiment', 'View Results', 'Settings']
for i, item in enumerate(sidebar_items):
    y_pos = 7 - i*0.8
    item_box = FancyBboxPatch((0.4, y_pos-0.3), 1.6, 0.4,
                             boxstyle="round,pad=0.03",
                             facecolor=COLOR_PRIMARY if i == 0 else 'white',
                             edgecolor=COLOR_PRIMARY if i == 0 else '#D1D5DB',
                             linewidth=1, alpha=0.7)
    ax.add_patch(item_box)
    ax.text(1.2, y_pos, item, ha='center', va='center',
            fontsize=9, color='white' if i == 0 else COLOR_TEXT)

# Main content area - Charts
chart_titles = ['Energy Consumption', 'Fairness Score', 'Convergence Rate', 'Carbon Footprint']
chart_positions = [(2.5, 5.5), (6, 5.5), (2.5, 2), (6, 2)]

for idx, (title, (x, y)) in enumerate(zip(chart_titles, chart_positions)):
    # Chart box
    chart_box = FancyBboxPatch((x-0.9, y-1.5), 3.2, 2.5,
                              boxstyle="round,pad=0.1",
                              edgecolor='#D1D5DB', facecolor='white',
                              linewidth=1.5)
    ax.add_patch(chart_box)
    
    # Chart title
    ax.text(x+0.6, y+0.75, title, ha='center', va='center',
            fontsize=11, fontweight='bold', color=COLOR_TEXT)
    
    # Mini chart representation
    if idx == 0:  # Energy - bar chart
        colors = ['#EF4444', '#F97316', '#FBBF24']
        for i, color in enumerate(colors):
            bar = mpatches.Rectangle((x-0.7+i*0.6, y-1.2), 0.5, 0.8+i*0.3,
                                    facecolor=color, alpha=0.7, edgecolor='none')
            ax.add_patch(bar)
    elif idx == 1:  # Fairness - line chart
        y_vals = [y-0.5, y-0.2, y+0.1, y-0.3]
        x_vals = [x-0.6, x-0.2, x+0.2, x+0.6]
        ax.plot(x_vals, y_vals, color=COLOR_SUCCESS, linewidth=3, marker='o', markersize=5)
    elif idx == 2:  # Convergence - curve
        x_curve = np.linspace(x-0.6, x+0.6, 50)
        y_curve = y - 0.3 * (1 - np.exp(-3 * (x_curve - (x-0.6)) / 1.2))
        ax.plot(x_curve, y_curve, color=COLOR_PRIMARY, linewidth=3)
    else:  # Carbon - gauge
        theta = np.linspace(0, np.pi, 100)
        r = 0.5
        ax.plot(x-0.5 + r*np.cos(theta), y-1.2 + r*np.sin(theta), 
                color=COLOR_WARNING, linewidth=3)

ax.text(5, 0.2, 'Real-time monitoring and interactive visualization of federated learning metrics',
        ha='center', va='center', fontsize=9, style='italic', color=COLOR_TEXT)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '1_dashboard.png'), dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print(f"✓ Dashboard image saved: {os.path.join(output_dir, '1_dashboard.png')}")
plt.close()

# ============================================================================
# 2. SYSTEM ARCHITECTURE IMAGE
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'System Architecture', ha='center', va='center',
        fontsize=20, fontweight='bold', color=COLOR_TEXT)

# Layer 1: Frontend
frontend_box = FancyBboxPatch((1, 7.5), 8, 1.2, boxstyle="round,pad=0.1",
                             edgecolor=COLOR_PRIMARY, facecolor='#DBEAFE',
                             linewidth=2)
ax.add_patch(frontend_box)
ax.text(5, 8.1, 'Frontend Layer', ha='center', va='center',
        fontsize=12, fontweight='bold', color=COLOR_PRIMARY)
ax.text(5, 7.75, 'HTML5 Dashboard • JavaScript • D3.js Charts • WebSocket Updates',
        ha='center', va='center', fontsize=9, color=COLOR_TEXT)

# Arrow down
arrow1 = FancyArrowPatch((5, 7.4), (5, 6.8), arrowstyle='->', 
                        mutation_scale=30, linewidth=2, color=COLOR_TEXT)
ax.add_patch(arrow1)

# Layer 2: API Gateway
api_box = FancyBboxPatch((1, 5.5), 8, 1.1, boxstyle="round,pad=0.1",
                        edgecolor=COLOR_SECONDARY, facecolor='#EDE9FE',
                        linewidth=2)
ax.add_patch(api_box)
ax.text(5, 6.1, 'API Gateway (Flask)', ha='center', va='center',
        fontsize=12, fontweight='bold', color=COLOR_SECONDARY)
ax.text(5, 5.7, '/api/simulations • /api/experiments • /api/metrics',
        ha='center', va='center', fontsize=9, color=COLOR_TEXT)

# Arrow down
arrow2 = FancyArrowPatch((5, 5.4), (5, 4.8), arrowstyle='->', 
                        mutation_scale=30, linewidth=2, color=COLOR_TEXT)
ax.add_patch(arrow2)

# Layer 3: Core Services (split into 3 sections)
# 3a: Simulation Engine
sim_box = FancyBboxPatch((0.5, 3.2), 2.8, 1.4, boxstyle="round,pad=0.1",
                        edgecolor=COLOR_SUCCESS, facecolor='#DCFCE7',
                        linewidth=2)
ax.add_patch(sim_box)
ax.text(1.9, 4.4, 'Simulation Engine', ha='center', va='center',
        fontsize=11, fontweight='bold', color=COLOR_SUCCESS)
ax.text(1.9, 4.0, 'RealisticSimulation\nGenerator', ha='center', va='center',
        fontsize=8, color=COLOR_TEXT)
ax.text(1.9, 3.4, 'Physics-based metrics', ha='center', va='center',
        fontsize=7, style='italic', color=COLOR_TEXT)

# 3b: Orchestration
orch_box = FancyBboxPatch((3.6, 3.2), 2.8, 1.4, boxstyle="round,pad=0.1",
                         edgecolor=COLOR_WARNING, facecolor='#FED7AA',
                         linewidth=2)
ax.add_patch(orch_box)
ax.text(5, 4.4, 'Orchestration', ha='center', va='center',
        fontsize=11, fontweight='bold', color=COLOR_WARNING)
ax.text(5, 4.0, 'Node Manager\nExperiment Manager', ha='center', va='center',
        fontsize=8, color=COLOR_TEXT)
ax.text(5, 3.4, 'Distributed coordination', ha='center', va='center',
        fontsize=7, style='italic', color=COLOR_TEXT)

# 3c: Metrics & Analytics
metrics_box = FancyBboxPatch((6.7, 3.2), 2.8, 1.4, boxstyle="round,pad=0.1",
                            edgecolor='#06B6D4', facecolor='#CFFAFE',
                            linewidth=2)
ax.add_patch(metrics_box)
ax.text(8.1, 4.4, 'Metrics & Eval', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#06B6D4')
ax.text(8.1, 4.0, 'Fairness • Energy\nCommunication', ha='center', va='center',
        fontsize=8, color=COLOR_TEXT)
ax.text(8.1, 3.4, 'Quality assurance', ha='center', va='center',
        fontsize=7, style='italic', color=COLOR_TEXT)

# Arrows from API to services
for x_pos in [1.9, 5, 8.1]:
    arrow = FancyArrowPatch((x_pos, 5.4), (x_pos, 4.6), arrowstyle='->', 
                           mutation_scale=25, linewidth=1.5, color=COLOR_TEXT)
    ax.add_patch(arrow)

# Arrow down from services
arrow3 = FancyArrowPatch((5, 3.1), (5, 2.5), arrowstyle='->', 
                        mutation_scale=30, linewidth=2, color=COLOR_TEXT)
ax.add_patch(arrow3)

# Layer 4: Data Layer (split into 2 sections)
# 4a: In-Memory Store
mem_box = FancyBboxPatch((1, 0.8), 3.5, 1.4, boxstyle="round,pad=0.1",
                        edgecolor='#8B5CF6', facecolor='#F3E8FF',
                        linewidth=2)
ax.add_patch(mem_box)
ax.text(2.75, 1.85, 'In-Memory Store', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#8B5CF6')
ax.text(2.75, 1.4, 'Experiments Cache\nResults Buffer', ha='center', va='center',
        fontsize=8, color=COLOR_TEXT)
ax.text(2.75, 0.95, 'Fast access & persistence', ha='center', va='center',
        fontsize=7, style='italic', color=COLOR_TEXT)

# 4b: Monitoring
mon_box = FancyBboxPatch((5.5, 0.8), 3.5, 1.4, boxstyle="round,pad=0.1",
                        edgecolor='#EC4899', facecolor='#FCE7F3',
                        linewidth=2)
ax.add_patch(mon_box)
ax.text(7.25, 1.85, 'Monitoring', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#EC4899')
ax.text(7.25, 1.4, 'Resource Monitor\nMetrics Logger', ha='center', va='center',
        fontsize=8, color=COLOR_TEXT)
ax.text(7.25, 0.95, 'System health & analytics', ha='center', va='center',
        fontsize=7, style='italic', color=COLOR_TEXT)

# Arrows from services to data layer
for x_pos in [2.75, 7.25]:
    arrow = FancyArrowPatch((5, 3.1), (x_pos, 2.2), arrowstyle='->', 
                           mutation_scale=20, linewidth=1.5, color=COLOR_TEXT, alpha=0.6)
    ax.add_patch(arrow)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '2_system_architecture.png'), dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"✓ System Architecture image saved: {os.path.join(output_dir, '2_system_architecture.png')}")
plt.close()

# ============================================================================
# 3. PROPOSED METHODOLOGY IMAGE
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'Proposed Methodology', ha='center', va='center',
        fontsize=20, fontweight='bold', color=COLOR_TEXT)

# Phase 1: Input Configuration
phase1_box = FancyBboxPatch((0.2, 7.5), 2.2, 1.2, boxstyle="round,pad=0.1",
                           edgecolor=COLOR_PRIMARY, facecolor='#DBEAFE',
                           linewidth=2)
ax.add_patch(phase1_box)
ax.text(1.3, 8.4, 'Phase 1', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLOR_PRIMARY)
ax.text(1.3, 8.0, 'Input Config', ha='center', va='center',
        fontsize=9, color=COLOR_TEXT)
ax.text(1.3, 7.6, '• Nodes\n• Strategy\n• Rounds', ha='center', va='center',
        fontsize=7, color=COLOR_TEXT)

# Arrow 1
arrow = FancyArrowPatch((2.4, 8.1), (3.4, 8.1), arrowstyle='->', 
                       mutation_scale=25, linewidth=2.5, color=COLOR_PRIMARY)
ax.add_patch(arrow)

# Phase 2: Simulation Engine
phase2_box = FancyBboxPatch((3.4, 7.5), 2.2, 1.2, boxstyle="round,pad=0.1",
                           edgecolor=COLOR_SUCCESS, facecolor='#DCFCE7',
                           linewidth=2)
ax.add_patch(phase2_box)
ax.text(4.5, 8.4, 'Phase 2', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLOR_SUCCESS)
ax.text(4.5, 8.0, 'Simulation', ha='center', va='center',
        fontsize=9, color=COLOR_TEXT)
ax.text(4.5, 7.6, '• Energy calc\n• Fairness\n• Convergence', ha='center', va='center',
        fontsize=7, color=COLOR_TEXT)

# Arrow 2
arrow = FancyArrowPatch((5.6, 8.1), (6.6, 8.1), arrowstyle='->', 
                       mutation_scale=25, linewidth=2.5, color=COLOR_SUCCESS)
ax.add_patch(arrow)

# Phase 3: Data Validation
phase3_box = FancyBboxPatch((6.6, 7.5), 2.2, 1.2, boxstyle="round,pad=0.1",
                           edgecolor=COLOR_WARNING, facecolor='#FED7AA',
                           linewidth=2)
ax.add_patch(phase3_box)
ax.text(7.7, 8.4, 'Phase 3', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLOR_WARNING)
ax.text(7.7, 8.0, 'Validation', ha='center', va='center',
        fontsize=9, color=COLOR_TEXT)
ax.text(7.7, 7.6, '• QA checks\n• NaN guard\n• Range check', ha='center', va='center',
        fontsize=7, color=COLOR_TEXT)

# Arrow down
arrow = FancyArrowPatch((7.7, 7.4), (7.7, 6.8), arrowstyle='->', 
                       mutation_scale=25, linewidth=2.5, color=COLOR_TEXT)
ax.add_patch(arrow)

# Phase 4: Storage Decision (diamond)
ax.text(7.7, 6.1, 'Transient or\nPersistent?', ha='center', va='center',
        fontsize=9, fontweight='bold', color=COLOR_TEXT, 
        bbox=dict(boxstyle='round,pad=0.5', facecolor=COLOR_LIGHT, edgecolor=COLOR_TEXT, linewidth=2))

# Left branch: Transient
arrow_left = FancyArrowPatch((7.0, 5.8), (4.0, 5.2), arrowstyle='->', 
                            mutation_scale=25, linewidth=2.5, color=COLOR_PRIMARY)
ax.add_patch(arrow_left)
ax.text(5.2, 5.6, 'Transient', ha='center', va='center',
        fontsize=8, style='italic', color=COLOR_PRIMARY, fontweight='bold')

trans_box = FancyBboxPatch((2.5, 3.8), 3, 1.2, boxstyle="round,pad=0.1",
                          edgecolor=COLOR_PRIMARY, facecolor='#DBEAFE',
                          linewidth=2)
ax.add_patch(trans_box)
ax.text(4, 4.65, 'Run Simulation', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLOR_PRIMARY)
ax.text(4, 4.2, 'Return results\nNo storage', ha='center', va='center',
        fontsize=8, color=COLOR_TEXT)

# Right branch: Persistent
arrow_right = FancyArrowPatch((8.4, 5.8), (7.0, 5.2), arrowstyle='->', 
                             mutation_scale=25, linewidth=2.5, color=COLOR_SUCCESS)
ax.add_patch(arrow_right)
ax.text(7.8, 5.6, 'Persistent', ha='center', va='center',
        fontsize=8, style='italic', color=COLOR_SUCCESS, fontweight='bold')

persist_box = FancyBboxPatch((5.5, 3.8), 3, 1.2, boxstyle="round,pad=0.1",
                            edgecolor=COLOR_SUCCESS, facecolor='#DCFCE7',
                            linewidth=2)
ax.add_patch(persist_box)
ax.text(7, 4.65, 'Execute Experiment', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLOR_SUCCESS)
ax.text(7, 4.2, 'Store with metadata\nRetrievable', ha='center', va='center',
        fontsize=8, color=COLOR_TEXT)

# Final output
output_box = FancyBboxPatch((2, 1.5), 6, 1.8, boxstyle="round,pad=0.1",
                           edgecolor='#8B5CF6', facecolor='#F3E8FF',
                           linewidth=2.5)
ax.add_patch(output_box)
ax.text(5, 3.0, 'Output Results', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#8B5CF6')
ax.text(5, 2.5, 'Final Metrics: Energy, Fairness, Convergence, Carbon, Communication',
        ha='center', va='center', fontsize=8, color=COLOR_TEXT)
ax.text(5, 2.0, 'Round Details: Per-round breakdown with timestamps and strategy info',
        ha='center', va='center', fontsize=8, color=COLOR_TEXT)
ax.text(5, 1.6, 'Metadata: Experiment ID, configuration, execution time, status',
        ha='center', va='center', fontsize=7, style='italic', color=COLOR_TEXT)

# Arrows to output
arrow_trans_out = FancyArrowPatch((4, 3.8), (4.5, 3.3), arrowstyle='->', 
                                 mutation_scale=20, linewidth=2, color=COLOR_TEXT)
ax.add_patch(arrow_trans_out)

arrow_pers_out = FancyArrowPatch((7, 3.8), (5.5, 3.3), arrowstyle='->', 
                                mutation_scale=20, linewidth=2, color=COLOR_TEXT)
ax.add_patch(arrow_pers_out)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '3_proposed_methodology.png'), dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"✓ Proposed Methodology image saved: {os.path.join(output_dir, '3_proposed_methodology.png')}")
plt.close()

# ============================================================================
# 4. EXPERIMENTAL SETUP IMAGE
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'Experimental Setup', ha='center', va='center',
        fontsize=20, fontweight='bold', color=COLOR_TEXT)

# Section 1: Node Configuration
config_header = FancyBboxPatch((0.2, 8.2), 4.6, 0.5, boxstyle="round,pad=0.05",
                              edgecolor=COLOR_PRIMARY, facecolor=COLOR_PRIMARY,
                              linewidth=2)
ax.add_patch(config_header)
ax.text(2.5, 8.45, 'Node Configuration', ha='center', va='center',
        fontsize=11, fontweight='bold', color='white')

# Node types
node_types = ['EDGE_NODE', 'COMPUTE_SERVER', 'GPU_CLUSTER', 'STORAGE_NODE']
node_power = ['15W', '50W', '150W', '25W']
node_cores = ['2 cores', '8 cores', '32 cores', '4 cores']

y_start = 7.9
for i, (ntype, power, cores) in enumerate(zip(node_types, node_power, node_cores)):
    y_pos = y_start - i * 0.7
    node_box = FancyBboxPatch((0.4, y_pos-0.3), 4.2, 0.5, boxstyle="round,pad=0.05",
                             edgecolor='#D1D5DB', facecolor=COLOR_LIGHT,
                             linewidth=1)
    ax.add_patch(node_box)
    ax.text(0.8, y_pos, ntype, ha='left', va='center',
            fontsize=8, fontweight='bold', color=COLOR_TEXT)
    ax.text(3.2, y_pos, f'{power} base', ha='center', va='center',
            fontsize=8, color=COLOR_TEXT)
    ax.text(4.2, y_pos, cores, ha='right', va='center',
            fontsize=8, color=COLOR_TEXT)

# Section 2: Strategy Profiles
strategy_header = FancyBboxPatch((5.2, 8.2), 4.6, 0.5, boxstyle="round,pad=0.05",
                                edgecolor=COLOR_SUCCESS, facecolor=COLOR_SUCCESS,
                                linewidth=2)
ax.add_patch(strategy_header)
ax.text(7.5, 8.45, 'Strategy Profiles', ha='center', va='center',
        fontsize=11, fontweight='bold', color='white')

strategies = ['Federated Learning', 'Centralized', 'Energy-Aware', 'Static']
fairness_vals = ['0.85±0.04', '0.75±0.06', '0.80±0.05', '0.65±0.08']
convergence_speed = ['Fast', 'Fastest', 'Balanced', 'Slow']

y_start = 7.9
for i, (strat, fair, conv) in enumerate(zip(strategies, fairness_vals, convergence_speed)):
    y_pos = y_start - i * 0.7
    strat_box = FancyBboxPatch((5.4, y_pos-0.3), 4.2, 0.5, boxstyle="round,pad=0.05",
                              edgecolor='#D1D5DB', facecolor=COLOR_LIGHT,
                              linewidth=1)
    ax.add_patch(strat_box)
    ax.text(5.8, y_pos, strat, ha='left', va='center',
            fontsize=8, fontweight='bold', color=COLOR_TEXT)
    ax.text(7.5, y_pos, f'Fair: {fair}', ha='center', va='center',
            fontsize=7, color=COLOR_TEXT)
    ax.text(9.0, y_pos, conv, ha='right', va='center',
            fontsize=7, color=COLOR_TEXT, style='italic')

# Section 3: Simulation Parameters
param_header = FancyBboxPatch((0.2, 4.2), 4.6, 0.5, boxstyle="round,pad=0.05",
                             edgecolor=COLOR_WARNING, facecolor=COLOR_WARNING,
                             linewidth=2)
ax.add_patch(param_header)
ax.text(2.5, 4.45, 'Simulation Parameters', ha='center', va='center',
        fontsize=11, fontweight='bold', color='white')

params = [
    ('Number of Rounds', '5-100'),
    ('Number of Nodes', '4-32'),
    ('Communication Type', 'Synchronous'),
    ('Data Distribution', 'IID & Non-IID')
]

y_start = 3.9
for i, (param_name, param_val) in enumerate(params):
    y_pos = y_start - i * 0.6
    param_box = FancyBboxPatch((0.4, y_pos-0.25), 4.2, 0.45, boxstyle="round,pad=0.05",
                              edgecolor='#D1D5DB', facecolor=COLOR_LIGHT,
                              linewidth=1)
    ax.add_patch(param_box)
    ax.text(0.8, y_pos, param_name, ha='left', va='center',
            fontsize=8, color=COLOR_TEXT, fontweight='bold')
    ax.text(4.2, y_pos, param_val, ha='right', va='center',
            fontsize=8, color=COLOR_SECONDARY)

# Section 4: Metrics Tracked
metrics_header = FancyBboxPatch((5.2, 4.2), 4.6, 0.5, boxstyle="round,pad=0.05",
                               edgecolor='#06B6D4', facecolor='#06B6D4',
                               linewidth=2)
ax.add_patch(metrics_header)
ax.text(7.5, 4.45, 'Metrics Tracked', ha='center', va='center',
        fontsize=11, fontweight='bold', color='white')

metrics = [
    ('Energy Consumption', '1.5-1.7 kWh/round'),
    ('Fairness Score', '0.65-0.92'),
    ('Convergence Rate', 'Exponential model'),
    ('Carbon Footprint', 'Regional intensity'),
    ('Communication OH', '45-48 MB/round'),
]

y_start = 3.9
for i, (metric_name, metric_range) in enumerate(metrics):
    y_pos = y_start - i * 0.55
    metric_box = FancyBboxPatch((5.4, y_pos-0.22), 4.2, 0.42, boxstyle="round,pad=0.05",
                               edgecolor='#D1D5DB', facecolor=COLOR_LIGHT,
                               linewidth=1)
    ax.add_patch(metric_box)
    ax.text(5.8, y_pos, metric_name, ha='left', va='center',
            fontsize=7, color=COLOR_TEXT, fontweight='bold')
    ax.text(9.2, y_pos, metric_range, ha='right', va='center',
            fontsize=7, color=COLOR_SECONDARY, style='italic')

# Bottom: Research Applications
research_header = FancyBboxPatch((0.2, 1.3), 9.6, 0.5, boxstyle="round,pad=0.05",
                                edgecolor='#8B5CF6', facecolor='#8B5CF6',
                                linewidth=2)
ax.add_patch(research_header)
ax.text(5, 1.55, 'Research Applications & Use Cases', ha='center', va='center',
        fontsize=11, fontweight='bold', color='white')

use_cases = [
    '• Strategy Performance Comparison',
    '• Energy-Efficiency vs Fairness Trade-offs',
    '• Scalability Analysis (nodes & rounds)',
    '• Network Topology Impact',
    '• Heterogeneous Device Simulation'
]

y_pos = 0.95
for use_case in use_cases:
    ax.text(0.5, y_pos, use_case, ha='left', va='center',
            fontsize=8, color=COLOR_TEXT)
    y_pos -= 0.25

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '4_experimental_setup.png'), dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f"✓ Experimental Setup image saved: {os.path.join(output_dir, '4_experimental_setup.png')}")
plt.close()

print("\n" + "="*70)
print("✓ All documentation images generated successfully!")
print("="*70)
print(f"\nLocation: {output_dir}")
print("\nGenerated images:")
print("  1. 1_dashboard.png - Dashboard UI layout and visualization")
print("  2. 2_system_architecture.png - System components and data flow")
print("  3. 3_proposed_methodology.png - Simulation workflow and logic")
print("  4. 4_experimental_setup.png - Configuration and metrics")
print("\nYou can now insert these images into your documentation!")
