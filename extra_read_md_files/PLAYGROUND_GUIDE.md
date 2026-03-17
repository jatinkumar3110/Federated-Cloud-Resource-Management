# Interactive Cloud Simulation Playground - User Guide

## Overview

The **Cloud Simulation Playground** is an interactive configuration layer built on top of the federated learning simulation platform. It allows users to:

- **Dynamically configure** heterogeneous cloud nodes (edge devices, user devices, compute servers, data center nodes)
- **Adjust node parameters** at runtime (CPU, memory, energy costs, SLA thresholds)
- **Select optimization strategies** and tune parameters
- **Run custom simulations** and observe real-time results
- **Visualize outcomes** including energy consumption, SLA violations, fairness metrics, and sustainability scores

This guide explains how to use the playground interface and API.

---

## Architecture

The playground is built with strict layer separation:

```
UI Layer              →  dashboard.html + JavaScript
                         Node configuration form, results display

API Layer             →  app.py (Flask routes)
                         /api/nodes/* (CRUD operations)
                         /api/simulations/run (execution)

Orchestration Layer   →  orchestration_nodes.py
                         Node configuration management
                         Scenario builder

Core Engine (Unchanged)
  - Federated learning (orchestration.py)
  - Strategies (strategies/*.py)
  - Metrics (metrics/*.py)
  - Visualizations (visualization/*.py)
```

### Design Principles

✅ **No business logic in UI** - All logic is server-side
✅ **No modifications to core** - Federated learning code is untouched
✅ **Reproducible** - Seeded random numbers, CPU-only
✅ **Research-grade** - Supports paper narrative and experimental design

---

## Getting Started

### 1. Start the Server

```bash
# Terminal 1: Start Flask application
cd Federated_Cloud_Dashboard
python app.py
```

The server will start on `http://localhost:5000`

### 2. Open the Dashboard

Navigate to **`http://localhost:5000`** in your browser.

You should see the dashboard with a new section: **"Cloud Node Configuration Playground"**

---

## Using the Playground

### Step 1: Add Nodes

In the left panel ("Add New Node"):

1. **Select Node Type** from dropdown:
   - **Edge Device** - Limited resources, high latency, low power
   - **User Device** - Mobile/laptop, variable capacity
   - **Compute Server** - Medium-high resources, good reliability
   - **Data Center Node** - Maximum resources, optimized

2. **Configure Parameters**:
   - **CPU Cores**: Number of processors (1-256)
   - **Memory (GB)**: RAM available (0.5-1024 GB)
   - **Energy Cost Factor**: Relative energy consumption multiplier (0.1-10x)
   - **SLA Threshold**: Target service level (0-100%)
   - **Region**: Energy intensity
     - `clean` - Renewable-heavy (0.1 kg CO2/kWh)
     - `mixed` - Grid average (0.5 kg CO2/kWh)
     - `fossil` - Coal-heavy (0.9 kg CO2/kWh)

3. **Click "Add Node"** to create the configuration

### Step 2: View Configured Nodes

In the right panel ("Configured Nodes"), you'll see a table with:

- **Node ID** - Unique identifier (e.g., `node_1`)
- **Type** - Edge Device, User Device, etc.
- **CPU** - Number of cores
- **Mem** - Memory in GB
- **Energy** - Cost factor (e.g., 1.0x)
- **SLA** - Threshold percentage
- **Actions** - Remove button

**Example configuration**:
```
ID      | Type           | CPU | Mem | Energy | SLA | Actions
--------|----------------|-----|-----|--------|-----|--------
node_1  | EDGE_DEVICE    | 2   | 4   | 0.5x   | 70% | Remove
node_2  | COMPUTE_SERVER | 8   | 32  | 1.5x   | 85% | Remove
node_3  | DATA_CENTER    | 16  | 64  | 2.0x   | 95% | Remove
```

### Step 3: Configure Simulation Parameters

In the "Run Custom Simulation" section:

1. **Strategy** - Select optimization approach:
   - `Static Allocation` - Rule-based (no learning)
   - `Centralized ML` - Global model (no privacy)
   - `Federated Learning` - Distributed, privacy-preserving
   - `Energy-Aware Heuristic` - Optimizes for efficiency

2. **Rounds** - Number of federated learning rounds (1-20)

3. **Optimization Weights** (from top section):
   - **α (Alpha)**: Energy weight - balance efficiency
   - **β (Beta)**: Fairness weight - balance resource utilization
   - **γ (Gamma)**: SLA weight - penalize violations

### Step 4: Run Simulation

Click **"Run Simulation with Current Nodes"**

The system will:
1. Validate your node configuration
2. Build a dynamic scenario with your nodes
3. Execute the simulation across all configured strategies
4. Generate visualizations
5. Display results

### Step 5: Interpret Results

After simulation completes, you'll see:

#### Simulation Parameters
- Strategy used
- Number of nodes
- Number of rounds
- Optimization weights (α, β, γ)

#### Strategy Metrics
For each strategy:
- **Energy**: Total kWh consumed
- **SLA Violations**: Count of SLA threshold violations
- **Fairness**: 0-1 score (higher = more fair)
- **Green Score**: 0-1 sustainability score (higher = greener)

#### Visualizations
- **Energy Plot** - Energy consumption across strategies
- **SLA Plot** - SLA violation counts
- **Fairness Plot** - Heatmap of fairness metrics
- **Dashboard Plot** - Multi-metric overview

### Step 6: Experiment & Refine

Try different configurations:

**Scenario A: Edge-Heavy**
- Many edge devices (low CPU, low memory)
- Few compute servers
- Compare strategy performance

**Scenario B: Server-Heavy**
- Many compute servers (high CPU, high memory)
- Few edge devices
- Observe strategy differences

**Scenario C: Heterogeneous**
- Mix of all node types
- Observe fairness and SLA trade-offs

**Scenario D: Green Region**
- All nodes in `clean` region
- Check sustainability impact

---

## REST API Reference

### Node Management

#### GET `/api/nodes`
Get all configured nodes.

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "node_id": "node_1",
      "node_type": "EDGE_DEVICE",
      "cpu_cores": 2,
      "memory_gb": 4.0,
      "energy_cost_factor": 0.5,
      "sla_threshold": 70,
      "region": "clean"
    }
  ],
  "count": 1
}
```

#### POST `/api/nodes`
Create a new node.

**Request**:
```json
{
  "node_type": "COMPUTE_SERVER",
  "cpu_cores": 8,
  "memory_gb": 32.0,
  "energy_cost_factor": 1.5,
  "sla_threshold": 85,
  "region": "mixed"
}
```

**Response** (201 Created):
```json
{
  "status": "success",
  "data": {
    "node_id": "node_2",
    "node_type": "COMPUTE_SERVER",
    ...
  }
}
```

#### PUT `/api/nodes/<node_id>`
Update a node's configuration.

**Request**:
```json
{
  "cpu_cores": 12,
  "sla_threshold": 90
}
```

#### DELETE `/api/nodes/<node_id>`
Remove a node.

#### POST `/api/nodes/clear`
Delete all nodes.

### Simulation

#### POST `/api/simulations/run`
Execute a simulation with configured nodes.

**Request**:
```json
{
  "strategy": "Federated Learning",
  "rounds": 5,
  "alpha": 0.4,
  "beta": 0.35,
  "gamma": 0.25
}
```

**Response**:
```json
{
  "status": "success",
  "simulation": {
    "strategy": "Federated Learning",
    "num_nodes": 3,
    "num_rounds": 5,
    "parameters": {
      "alpha": 0.4,
      "beta": 0.35,
      "gamma": 0.25
    }
  },
  "results": {
    "Federated Learning": {
      "total_energy": 45.23,
      "avg_energy": 15.08,
      "energy_std": 2.34,
      "sla_violations": 2,
      "fairness_score": 0.92,
      "communication_mb": 23.45,
      "green_score": 0.85
    }
  },
  "visualizations": {
    "energy_plot": "temp_plots/custom_energy.png",
    "sla_plot": "temp_plots/custom_sla.png",
    "fairness_plot": "temp_plots/custom_fairness.png",
    "dashboard_plot": "temp_plots/custom_dashboard.png"
  }
}
```

---

## Python API

### Programmatic Usage

```python
from orchestration_nodes import get_nodes_manager
from experiments.scenario_manager import Scenario
from experiments.experiment_runner import ExperimentRunner

# Get manager
manager = get_nodes_manager()

# Add nodes
node1 = manager.add_node(
    node_type="EDGE_DEVICE",
    cpu_cores=2,
    memory_gb=4.0,
    energy_cost_factor=0.5,
    sla_threshold=70,
    region="clean"
)

# Get all nodes
nodes = manager.get_all_nodes()

# Convert to simulation nodes
sim_nodes = manager.to_nodes()

# Create scenario
scenario = Scenario(
    name="my_scenario",
    description="Custom configuration",
    num_rounds=5,
    num_nodes_per_type={},
    strategies=["Federated Learning"],
    custom_nodes=sim_nodes,
    alpha=0.4,
    beta=0.35,
    gamma=0.25
)

# Run experiment
runner = ExperimentRunner(verbose=False)
results = runner.run_experiment(scenario)

# Access results
for strategy, metrics in results.items():
    print(f"{strategy}: {metrics['total_energy']} kWh")
```

---

## Playground Features

### Supported Node Types

| Type | CPU | Memory | Energy | Purpose |
|------|-----|--------|--------|---------|
| **EDGE_DEVICE** | 2 | 4 GB | 0.5x | IoT, sensors, local processing |
| **USER_DEVICE** | 4 | 8 GB | 0.8x | Laptops, smartphones |
| **COMPUTE_SERVER** | 16 | 32 GB | 1.5x | General-purpose servers |
| **DATA_CENTER_NODE** | 32 | 64 GB | 2.0x | High-performance clusters |

*Note: CPU and Memory show typical profiles. You can customize these values.*

### Supported Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Static Allocation** | Fixed rules | Baseline comparison |
| **Centralized ML** | Global model at server | Privacy-unaware baseline |
| **Federated Learning** | Distributed learning | Privacy-preserving |
| **Energy-Aware Heuristic** | Efficiency-first | Green computing |

### Metrics Explained

**Total Energy** (kWh)
- Cumulative energy across all rounds
- Lower is better (more efficient)
- Determined by: node hardware, utilization, duration

**SLA Violations**
- Count of times resource constraints exceed thresholds
- Lower is better (more reliable)
- Penalized by γ (gamma) weight

**Fairness Score** (0-1)
- Jain Index of resource allocation
- 1.0 = perfect fairness (all nodes treated equally)
- Higher is better (more equitable)

**Green Score** (0-1)
- Combination of energy efficiency and carbon intensity
- 1.0 = optimal (renewable, efficient)
- 0.0 = worst (fossil, wasteful)
- Depends on: region, energy consumption

---

## Tips & Best Practices

### For Research

1. **Reproducibility**: Seeds are fixed (42). Results are deterministic.
2. **Batch Experiments**: Use the API to script multiple scenarios.
3. **Parameter Sweeps**: Vary α, β, γ to explore trade-offs.
4. **Node Heterogeneity**: Mix different types to study fairness.

### For Presentation

1. **Start simple**: 2-3 nodes to explain concepts
2. **Show trade-offs**: Compare energy vs. fairness
3. **Highlight sustainability**: Use `clean` regions to demonstrate green impact
4. **Quantify results**: Show numeric metrics alongside visualizations

### Common Scenarios

**Scenario: Edge Computing Efficiency**
```
Nodes: 5x EDGE_DEVICE (low power)
Strategy: Energy-Aware Heuristic
Metric: Compare energy savings vs. Federated Learning
```

**Scenario: Fairness in Heterogeneous Networks**
```
Nodes: 2x EDGE + 2x COMPUTE + 1x DATA_CENTER
Strategy: All strategies
Metric: Fairness score and SLA violations
```

**Scenario: Green Cloud**
```
Nodes: 4x nodes, all in "clean" region
Strategy: Federated Learning
Metric: Green score and carbon footprint
```

---

## Troubleshooting

### "No nodes configured"
- Add at least one node before running simulation
- Use "Add Node" button to create configuration

### "Invalid strategy"
- Ensure strategy name matches exactly:
  - `Static Allocation`
  - `Centralized ML`
  - `Federated Learning`
  - `Energy-Aware Heuristic`

### "Simulation failed"
- Check node parameters (CPU > 0, Memory > 0)
- Ensure at least one strategy is selected
- Check browser console for error details

### Visualizations not showing
- Run simulation again (may take a few seconds)
- Check if temp_plots/ directory exists
- Refresh browser if needed

---

## Integration with Research

The playground supports the research narrative:

> "An interactive simulation interface enables dynamic configuration of heterogeneous cloud nodes, allowing exploratory evaluation of federated resource management strategies under varying system conditions."

**How it demonstrates this**:

1. ✅ **Interactive**: Users configure nodes via UI/API
2. ✅ **Dynamic**: Parameters changed at runtime
3. ✅ **Heterogeneous**: Different node types with varied hardware
4. ✅ **Exploratory**: Compare multiple strategies and settings
5. ✅ **Evaluation**: Comprehensive metrics (energy, fairness, SLA, green)
6. ✅ **Reproducible**: Deterministic, seeded random numbers

---

## Advanced Usage

### Custom Node Profiles

While the playground uses standard NodeType profiles, you can extend it:

```python
# In orchestration_nodes.py
# Modify NodeType to add custom profiles
```

### Scenario Persistence

Save/load node configurations:

```python
manager = get_nodes_manager()
config_dict = manager.to_dict()

# Save to file
import json
with open('scenario.json', 'w') as f:
    json.dump(config_dict, f)

# Load later
new_manager = NodesManager()
with open('scenario.json', 'r') as f:
    new_manager.from_dict(json.load(f))
```

### Batch Automation

Run multiple scenarios programmatically:

```python
scenarios = [
    {"name": "edge_heavy", "nodes": [EDGE, EDGE, USER]},
    {"name": "compute_heavy", "nodes": [COMPUTE, COMPUTE, DATA_CENTER]},
    {"name": "balanced", "nodes": [EDGE, USER, COMPUTE, DATA_CENTER]}
]

for scenario_config in scenarios:
    manager = NodesManager()
    # Add nodes...
    # Run simulation...
    # Save results...
```

---

## Support & Documentation

- **Main README**: [README.md](README.md)
- **API Reference**: [API_REFERENCE.md](API_REFERENCE.md)
- **System Status**: [UPGRADE_COMPLETE.md](UPGRADE_COMPLETE.md)
- **Quickstart**: [QUICKSTART.md](QUICKSTART.md)

---

## Version Info

- **Playground Version**: 2.0
- **Core System**: v2.0 (7-phase upgrade)
- **Node Manager**: orchestration_nodes.py
- **Last Updated**: January 21, 2026

---

**Ready to explore? Start by opening `http://localhost:5000` and configuring your first nodes!**
