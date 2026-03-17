# Quick Start Guide - V4.0

## What's New?

✨ **Complete separation** between interactive simulations (transient) and scientific experiments (persistent)  
✨ **Realistic data** generation with proper physics-based calculations  
✨ **Research-grade** metrics with no NaN values  
✨ **New UI button** for executing and storing experiments  

---

## Quick Start (5 Minutes)

### 1. Add Nodes
```
Dashboard → Nodes → Add nodes
Or: POST /api/nodes with your configuration
```

### 2. Run Quick Simulation
```
Click "Run Simulation" button
Select strategy and number of rounds
Results appear instantly (not saved)
```

### 3. Execute Permanent Experiment
```
Click "Execute Experiment" button
Name your experiment
Results are saved with ID
Can be retrieved and compared later
```

### 4. View Results
```
Dashboard shows charts and metrics
Metrics include:
  - Energy consumption (kWh)
  - Fairness score (0-1)
  - Convergence metric (0-1)
  - Carbon footprint (kg CO2)
  - Communication overhead (MB)
  - SLA violations (count)
```

---

## API Quick Reference

### Transient Simulation (No Storage)
```bash
curl -X POST http://localhost:5000/api/simulations/run \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "Federated Learning",
    "rounds": 5
  }'
```

### Persistent Experiment (Stored)
```bash
curl -X POST http://localhost:5000/api/experiments/execute \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Experiment",
    "strategy": "Energy-Aware Heuristic",
    "rounds": 10
  }'
```

### List All Experiments
```bash
curl http://localhost:5000/api/experiments/list
```

### Get Experiment Details
```bash
curl http://localhost:5000/api/experiments/1
```

### Delete Experiment
```bash
curl -X DELETE http://localhost:5000/api/experiments/delete/1
```

---

## Strategies Explained

| Strategy | Fairness | Speed | Energy | Best For |
|----------|----------|-------|--------|----------|
| Static Allocation | Medium (0.73) | Fast | Medium | Baseline |
| Centralized ML | Medium (0.79) | Fastest | Low | Efficiency |
| Federated Learning | High (0.92) | Moderate | Low | Fairness |
| Energy-Aware | High (0.90) | Moderate | Medium | Balance |

---

## Key Metrics

**Energy (kWh)**
- Per-round consumption
- Calculated from node power × utilization
- Regional carbon intensity applied

**Fairness Score (0-1)**
- Higher = more equitable distribution
- Strategy-dependent
- Federated Learning is fairest

**Convergence Metric (0-1)**
- Higher = better solution quality
- Normalized convergence curve
- Exponential improvement over rounds

**Carbon Footprint (kg CO2)**
- Energy × regional carbon intensity
- Clean (0.1), Mixed (0.4), Fossil (0.8) kg CO2/kWh
- Sustainability assessment

---

## Important Differences

### Run Simulation (Transient)
- Fast (100-150ms)
- Results NOT saved
- No persistence overhead
- Good for exploration
- Use for: Quick feedback, testing parameters

### Execute Experiment (Persistent)
- Slightly slower (120-150ms)
- Results ARE saved
- Can be retrieved later
- Good for comparison
- Use for: Scientific analysis, comparative studies

---

## Common Tasks

### Compare Two Strategies
```python
import requests

# Run first strategy
r1 = requests.post('http://localhost:5000/api/simulations/run',
    json={'strategy': 'Federated Learning', 'rounds': 10})

# Run second strategy  
r2 = requests.post('http://localhost:5000/api/simulations/run',
    json={'strategy': 'Energy-Aware Heuristic', 'rounds': 10})

# Compare metrics
m1 = r1.json()['final_metrics']
m2 = r2.json()['final_metrics']

print(f"Fairness: {m1['fairness_score']:.3f} vs {m2['fairness_score']:.3f}")
print(f"Energy: {m1['avg_energy']:.3f} vs {m2['avg_energy']:.3f} kWh")
```

### Save Experiment for Later
```python
import requests

# Execute and save
r = requests.post('http://localhost:5000/api/experiments/execute',
    json={
        'name': 'Production_FedLearning_Q1_2026',
        'strategy': 'Federated Learning',
        'rounds': 20
    })

exp_id = r.json()['experiment_id']
print(f"Saved as Experiment {exp_id}")

# Retrieve later
r = requests.get(f'http://localhost:5000/api/experiments/{exp_id}')
results = r.json()['experiment']['results']
print(f"Energy: {results['final_metrics']['avg_energy']:.3f} kWh")
```

### Analyze Energy by Region
```python
# Get experiment
r = requests.get('http://localhost:5000/api/experiments/1')
results = r.json()['experiment']['results']

# Extract regional breakdown
energy_by_region = results['energy_by_region']
print("Regional Energy Distribution:")
for region, energy in energy_by_region.items():
    print(f"  {region}: {energy:.3f} kWh")

# Calculate carbon
intensity = {'clean': 0.1, 'mixed': 0.4, 'fossil': 0.8}
total_carbon = sum(energy_by_region[r] * intensity[r] for r in energy_by_region)
print(f"\nTotal Carbon: {total_carbon:.3f} kg CO2")
```

---

## Troubleshooting

### "No nodes configured" Error
→ Add nodes via Dashboard or API before running simulation

### Simulation returns 400 error
→ Check strategy name (must be exact match: "Federated Learning", etc.)

### Experiment not saving
→ Ensure POST /api/experiments/execute, not /api/simulations/run

### NaN values in results
→ Restart server to refresh code, all metrics should be valid

### Performance is slow
→ Consider upgrading to database-backed storage if many experiments

---

## Configuration

### Adjust Node Parameters
```bash
POST /api/nodes
{
  "node_type": "DATA_CENTER_NODE",      # Required
  "cpu_cores": 32,                      # Required
  "memory_gb": 128,                     # Required
  "energy_cost_factor": 1.0,            # Required
  "sla_threshold": 99.9,                # Required
  "region": "clean"                     # Optional: clean, mixed, fossil
}
```

### Customize Simulation Parameters
```bash
POST /api/simulations/run
{
  "strategy": "Federated Learning",     # Required
  "rounds": 5,                          # Required
  "alpha": 0.4,                         # Optional (default 0.4)
  "beta": 0.35,                         # Optional (default 0.35)
  "gamma": 0.25                         # Optional (default 0.25)
}
```

---

## Documentation

- **Full Guide**: See `IMPLEMENTATION_SUMMARY_V4.md`
- **Completion Report**: See `COMPLETION_REPORT_V4.md`
- **Executive Summary**: See `EXECUTIVE_SUMMARY_V4.md`

---

## Support

**All endpoints tested and working ✅**  
**All metrics validated ✅**  
**All documentation complete ✅**  

Questions? Check the comprehensive guides or Flask logs for error details.

---

*Version 4.0 - January 22, 2026*  
*Status: Production Ready ✅*
