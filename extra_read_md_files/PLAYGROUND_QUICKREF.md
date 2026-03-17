# Cloud Simulation Playground - Quick Reference

## What is the Playground?

An **interactive web interface** for configuring and testing federated learning strategies on custom cloud node configurations.

## Quick Start (2 minutes)

```bash
# 1. Start server
python app.py

# 2. Open browser
# http://localhost:5000

# 3. Add nodes using the form
# - Select node type (EDGE, COMPUTE, etc.)
# - Set CPU, Memory, Energy, SLA
# - Click "Add Node"

# 4. Run simulation
# - Pick strategy (Federated Learning recommended)
# - Click "Run Simulation"
# - See results & visualizations
```

## Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  Federated Cloud Dashboard - Playground Section          │
├────────────────────────┬────────────────────────────────┤
│   Add New Node Form    │   Configured Nodes Table       │
│  - Type dropdown       │   - Lists all added nodes      │
│  - CPU cores field     │   - Remove buttons             │
│  - Memory GB field     │   - Shows config summary       │
│  - Energy factor       │                                │
│  - SLA threshold       │  Node Count: 3                 │
│  - Region selector     │                                │
│  [Add Node] [Clear]    │                                │
├────────────────────────┴────────────────────────────────┤
│  Run Custom Simulation                                   │
│  - Strategy dropdown (Federated Learning)               │
│  - Rounds input (5)                                      │
│  [Run Simulation with Current Nodes]                    │
├─────────────────────────────────────────────────────────┤
│  Simulation Results (after running)                      │
│  - Metrics summary table                                │
│  - 4 visualizations (Energy, SLA, Fairness, Dashboard)  │
└─────────────────────────────────────────────────────────┘
```

## Node Configuration

### Node Types

| Type | Purpose |
|------|---------|
| **EDGE_DEVICE** | IoT, local devices, low power |
| **USER_DEVICE** | Laptops, smartphones |
| **COMPUTE_SERVER** | Mid-range servers |
| **DATA_CENTER_NODE** | High-performance clusters |

### Key Parameters

- **CPU Cores** (1-256): Compute capacity
- **Memory (GB)** (0.5-1024): RAM available
- **Energy Cost** (0.1-10x): Relative power consumption
- **SLA Threshold** (0-100%): Target resource availability
- **Region** (clean/mixed/fossil): Carbon intensity

### Example Configurations

**Edge Device**
```
CPU: 2 | Memory: 4GB | Energy: 0.5x | SLA: 70% | Region: clean
```

**Compute Server**
```
CPU: 8 | Memory: 32GB | Energy: 1.5x | SLA: 85% | Region: mixed
```

**Data Center**
```
CPU: 16 | Memory: 64GB | Energy: 2.0x | SLA: 95% | Region: mixed
```

## Simulation Parameters

### Strategies

- **Static Allocation**: Fixed rules (no learning)
- **Centralized ML**: Global model (baseline)
- **Federated Learning**: Distributed & private (recommended)
- **Energy-Aware**: Efficiency-focused

### Optimization Weights

- **α (Alpha)** [0-1]: Energy weight (default 0.4)
- **β (Beta)** [0-1]: Fairness weight (default 0.35)
- **γ (Gamma)** [0-1]: SLA penalty (default 0.25)

Adjust sliders to change strategy preferences.

## Metrics Explained

| Metric | Meaning | Better |
|--------|---------|--------|
| **Energy (kWh)** | Total power consumed | Lower |
| **SLA Violations** | Broken service levels | Lower |
| **Fairness** | Resource distribution equality | Higher (→1.0) |
| **Green Score** | Sustainability (energy + carbon) | Higher (→1.0) |

## API Endpoints

### Node Management

```
GET    /api/nodes              # List all nodes
POST   /api/nodes              # Add node
PUT    /api/nodes/<id>         # Update node
DELETE /api/nodes/<id>         # Remove node
POST   /api/nodes/clear        # Clear all
```

### Simulation

```
POST   /api/simulations/run     # Run with configured nodes
```

## Common Use Cases

### Test 1: Edge Computing Efficiency
```
Setup: 5 x EDGE_DEVICE (low power)
Strategy: Energy-Aware Heuristic
Compare: Energy vs. baseline
```

### Test 2: Fairness in Heterogeneous Networks
```
Setup: 2 EDGE + 2 COMPUTE + 1 DATA_CENTER
Strategies: All 4
Metric: Fairness + SLA trade-off
```

### Test 3: Green Cloud
```
Setup: 4 nodes, all "clean" region
Strategy: Federated Learning
Metric: Green score & carbon footprint
```

### Test 4: Scalability
```
Setup: Gradually increase nodes (1→5→10)
Strategy: Federated Learning
Metric: How energy scales with nodes
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No nodes configured" | Click "Add Node" first |
| Strategy not found | Check exact spelling in dropdown |
| Simulation hangs | Wait 10-30 seconds (depends on nodes/rounds) |
| Visualizations blank | Refresh browser after simulation |
| Server won't start | Port 5000 in use? Kill other Flask processes |

## Files

| File | Purpose |
|------|---------|
| **orchestration_nodes.py** | Node manager backend |
| **app.py** | Flask API endpoints |
| **templates/dashboard.html** | UI (includes playground section) |
| **PLAYGROUND_GUIDE.md** | Full documentation |
| **API_REFERENCE.md** | Complete API spec |

## Code Examples

### Via Browser
1. Open http://localhost:5000
2. Fill form and click "Add Node"
3. Select strategy and click "Run"
4. View results

### Via cURL
```bash
# Add node
curl -X POST http://localhost:5000/api/nodes \
  -H "Content-Type: application/json" \
  -d '{
    "node_type": "COMPUTE_SERVER",
    "cpu_cores": 8,
    "memory_gb": 32,
    "energy_cost_factor": 1.5,
    "sla_threshold": 85,
    "region": "mixed"
  }'

# Get all nodes
curl http://localhost:5000/api/nodes

# Run simulation
curl -X POST http://localhost:5000/api/simulations/run \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "Federated Learning",
    "rounds": 5
  }'
```

### Via Python
```python
from orchestration_nodes import get_nodes_manager
from experiments.scenario_manager import Scenario
from experiments.experiment_runner import ExperimentRunner

manager = get_nodes_manager()
manager.add_node("EDGE_DEVICE", 2, 4.0, 0.5, 70, "clean")
manager.add_node("COMPUTE_SERVER", 8, 32.0, 1.5, 85, "mixed")

nodes = manager.to_nodes()
scenario = Scenario(
    name="test",
    description="Test",
    num_rounds=5,
    num_nodes_per_type={},
    strategies=["Federated Learning"],
    custom_nodes=nodes
)

runner = ExperimentRunner(verbose=False)
results = runner.run_experiment(scenario)
```

## Key Features

✅ **Interactive** - Configure nodes via UI
✅ **No Code** - No Python knowledge needed  
✅ **Real-Time** - Instant simulation results
✅ **Heterogeneous** - Mix different node types
✅ **Reproducible** - Seeded randomness
✅ **Research-Grade** - Rigorous metrics
✅ **Multi-Strategy** - Compare 4 approaches
✅ **Visualizations** - Charts and plots

## Next Steps

1. **Start server**: `python app.py`
2. **Open UI**: http://localhost:5000
3. **Add 3 nodes**: Edge, Compute, DataCenter
4. **Run test**: Federated Learning, 5 rounds
5. **Review results**: Energy, fairness, SLA
6. **Experiment**: Try different configurations

---

**For detailed info, see PLAYGROUND_GUIDE.md**
