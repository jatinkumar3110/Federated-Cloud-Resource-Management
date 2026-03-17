# Federated Cloud Dashboard

A professional research system for simulating, analyzing, and comparing federated learning strategies in distributed cloud environments.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Open browser
http://localhost:5000
```

## What's Included

- **simulation_data_generator.py** - Core physics-based simulation engine with realistic energy, fairness, and convergence metrics
- **app.py** - Flask REST API with 5 endpoints for simulations and experiments
- **dashboard_v3.html** - Interactive web dashboard with visualizations
- **requirements.txt** - Python dependencies
- **TECHNICAL_DOCUMENTATION.md** - Complete technical specification

## Key Features

✓ **4 Federated Learning Strategies**: Static, Centralized, Federated, Energy-Aware  
✓ **Realistic Metrics**: Physics-based energy, fairness, convergence, carbon footprint  
✓ **Transient Simulations**: Quick interactive exploration (100ms)  
✓ **Persistent Experiments**: Store and compare results for research  
✓ **Interactive Dashboard**: Real-time charts and strategy comparison  
✓ **Research-Ready**: Proper semantics, reproducible, extensible  

## API Endpoints

```bash
# Run a quick simulation (non-persistent)
POST /api/simulations/run
{"strategy": "Federated Learning", "rounds": 5}

# Execute and save an experiment
POST /api/experiments/execute
{"name": "Exp_1", "strategy": "Federated Learning", "rounds": 10}

# List all experiments
GET /api/experiments/list

# Get experiment details
GET /api/experiments/<id>

# Delete experiment
DELETE /api/experiments/delete/<id>
```

## System Architecture

```
Dashboard UI (web browser)
         ↓
    Flask REST API
         ↓
RealisticSimulationGenerator
         ↓
    Node Configuration
         ↓
    Data Storage
```

## Research Applications

- Compare federated learning strategies
- Analyze energy-fairness tradeoffs
- Study convergence behavior
- Track sustainability metrics
- Publish reproducible results

## Documentation

See **TECHNICAL_DOCUMENTATION.md** for:
- Complete architecture explanation
- Data generation algorithms
- API specification
- Configuration options
- Performance characteristics
- Research applications

## System Requirements

- Python 3.8+
- Flask 2.3+
- NumPy 1.24+
- Modern web browser

## Configuration

Edit constants in `simulation_data_generator.py`:
- `CARBON_INTENSITY` - Regional energy mix
- `NODE_POWER_BASE` - Node energy profiles
- `STRATEGY_FAIRNESS` - Strategy-specific fairness profiles
- `STRATEGY_CONVERGENCE` - Convergence behavior per strategy

## For Collaboration

This is a research-grade system designed for:
- Publishing peer-reviewed papers
- Reproducible experiments
- Strategy comparison studies
- Energy-fairness analysis
- Sustainability research

All code is clean, well-documented, and extensible.

---

**Version**: 4.0  
**Status**: Production Ready  
**License**: [Your License]  

For detailed technical information, see TECHNICAL_DOCUMENTATION.md
