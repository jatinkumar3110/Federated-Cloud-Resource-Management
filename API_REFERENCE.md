# API Reference - Federated Cloud Dashboard v2.0

## Overview

The REST API provides access to all simulation, experiment, and metrics capabilities. All endpoints return JSON responses.

---

## Base Information

**Base URL**: `http://localhost:5000`

**Response Format**:
```json
{
  "status": "success|error",
  "data": {...},
  "message": "error message (if applicable)"
}
```

---

## Endpoints

### Dashboard & Configuration

#### GET `/api/dashboard/metadata`
Returns dashboard metadata including available node types, strategies, and default parameters.

**Response**:
```json
{
  "status": "success",
  "data": {
    "node_types": [
      {
        "name": "edge_device",
        "value": "EDGE_DEVICE",
        "description": "Edge device (2 CPU, 4GB)"
      },
      ...
    ],
    "strategies": [
      {
        "name": "Static Allocation",
        "value": "Static Allocation",
        "description": "Fixed allocation rules"
      },
      ...
    ],
    "defaults": {
      "num_rounds": 5,
      "alpha": 0.4,
      "beta": 0.35,
      "gamma": 0.25
    }
  }
}
```

---

### Experiments

#### GET `/api/experiments/scenarios`
Get list of available experiment scenarios.

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "name": "small_scale",
      "display_name": "Small Scale",
      "description": "Small heterogeneous deployment",
      "num_rounds": 5,
      "num_nodes": 3,
      "strategies": ["Static Allocation", "Federated Learning", ...]
    },
    ...
  ]
}
```

#### POST `/api/experiments/run`
Execute a single experiment scenario.

**Request**:
```json
{
  "scenario_name": "small_scale",
  "export_csv": false
}
```

**Response**:
```json
{
  "status": "success",
  "scenario": "small_scale",
  "data": {
    "Static Allocation": {
      "total_energy": 29.82,
      "avg_energy": 14.91,
      "energy_std": 0.15,
      "sla_violations": 0,
      "fairness_score": 1.0,
      "communication_mb": 18.76,
      "green_score": 0.999
    },
    "Federated Learning": {
      ...
    }
  },
  "csv_file": "experiment_results/small_scale_1234567890.csv"
}
```

---

### Metrics

#### POST `/api/metrics/fairness`
Compute fairness metrics for resource allocations.

**Request**:
```json
{
  "node_allocations": {
    "node_1": 0.3,
    "node_2": 0.3,
    "node_3": 0.4
  }
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "jain_index": 0.98,
    "gini_coefficient": 0.067,
    "allocation_gap": 0.1,
    "coefficient_of_variation": 0.105
  }
}
```

#### POST `/api/metrics/communication`
Compute communication overhead metrics.

**Request**:
```json
{
  "num_nodes": 4,
  "num_rounds": 5,
  "model_size_bytes": 512
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "per_round_bytes": 4608,
    "total_bytes": 23040,
    "total_megabytes": 0.022,
    "redundancy_factor": 45.0
  }
}
```

#### POST `/api/metrics/sustainability`
Compute sustainability metrics.

**Request**:
```json
{
  "total_energy": 50.0,
  "region": "mixed"
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_energy_kwh": 0.05,
    "carbon_kg": 0.025,
    "region": "mixed",
    "green_score": 0.998
  }
}
```

---

### Health Check

#### GET `/health`
Check API health and available features.

**Response**:
```json
{
  "status": "healthy",
  "service": "Federated Cloud Dashboard v2",
  "features": {
    "optimization": true,
    "heterogeneous_nodes": true,
    "multiple_strategies": true,
    "fairness_metrics": true,
    "communication_metrics": true,
    "sustainability_metrics": true,
    "visualizations": true,
    "experiment_automation": true
  }
}
```

---

### Legacy Endpoints (v1.0 - Preserved)

#### POST `/api/simulation/start`
Start federated learning simulation.

**Request**:
```json
{
  "alpha": 0.4,
  "beta": 0.35,
  "gamma": 0.25,
  "sla_cpu": 80,
  "sla_memory": 85
}
```

#### GET `/api/metrics/current`
Get current system metrics.

#### GET `/api/model/state`
Get global model state (weights and bias).

---

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Invalid parameter value: ..."
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Error description"
}
```

---

## Example Usage

### Python Requests Library

```python
import requests

# Get metadata
response = requests.get("http://localhost:5000/api/dashboard/metadata")
metadata = response.json()

# Run experiment
response = requests.post(
    "http://localhost:5000/api/experiments/run",
    json={"scenario_name": "small_scale", "export_csv": True}
)
results = response.json()

# Compute fairness
response = requests.post(
    "http://localhost:5000/api/metrics/fairness",
    json={"node_allocations": {"n1": 0.3, "n2": 0.7}}
)
fairness = response.json()
```

### cURL

```bash
# Get metadata
curl -X GET http://localhost:5000/api/dashboard/metadata

# Run experiment
curl -X POST http://localhost:5000/api/experiments/run \
  -H "Content-Type: application/json" \
  -d '{"scenario_name": "small_scale"}'

# Check health
curl -X GET http://localhost:5000/health
```

---

## Data Types

### Node Type Values
- `"edge_device"` - EDGE_DEVICE
- `"user_device"` - USER_DEVICE
- `"compute_server"` - COMPUTE_SERVER
- `"data_center_node"` - DATA_CENTER_NODE

### Strategy Names
- `"Static Allocation"` - Fixed rules
- `"Centralized ML"` - Global model
- `"Federated Learning"` - Distributed learning
- `"Energy-Aware Heuristic"` - Efficiency heuristics

### Regions
- `"clean"` - Renewable-heavy (0.1 kg CO2/kWh)
- `"mixed"` - Grid average (0.5 kg CO2/kWh)
- `"fossil"` - Coal-heavy (0.9 kg CO2/kWh)

---

## Rate Limiting

No rate limiting currently implemented. Experiment execution may take time depending on:
- Number of nodes
- Number of rounds
- Number of strategies

---

## Authentication

Currently no authentication. For production, implement JWT tokens or OAuth2.

---

## Versioning

Current version: **2.0** (Complete Upgrade)

Legacy support: **1.0** routes preserved for backward compatibility

---

## Support

For issues or questions, refer to the main README.md or project documentation.

---

*API Documentation - Federated Cloud Dashboard v2.0*
*Last Updated: January 21, 2026*
