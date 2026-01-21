# Federated Learning–Driven Resource Management for Cloud Computing Environments

## Project Overview

A research-grade capstone project implementing **federated learning** for privacy-preserving resource management in cloud environments. The system trains a global model across distributed clients without centralizing raw data.

**Key Features:**
- ✅ Federated averaging (FedAvg) algorithm
- ✅ Privacy-preserving distributed training
- ✅ Multi-objective optimization (energy, cost, SLA)
- ✅ Real-time resource monitoring
- ✅ Interactive web dashboard
- ✅ Reproducible experiments (CPU-only, fixed seeds)
- ✅ Exam-ready, modular, callable code

---

## Architecture

### Layered Design (Strict SRP)

```
┌─────────────────────────────────────┐
│  Web Orchestration Layer (app.py)   │  ← Flask routes only
├─────────────────────────────────────┤
│  Orchestration Layer (orchestration.py) │ ← Pipeline coordinator
├─────────────────────────────────────┤
│  Federated Learning Layer           │
│  ├── model.py                       │  ← FederatedNeuralNetwork
│  └── trainer.py                     │  ← FederatedClient, FederatedServer
├─────────────────────────────────────┤
│  Metrics & Evaluation Layer         │
│  └── evaluator.py                   │  ← MetricsEvaluator
├─────────────────────────────────────┤
│  Simulation Layer                   │
│  ├── workload.py                    │  ← WorkloadGenerator
│  └── resource_monitor.py            │  ← ResourceMonitor
└─────────────────────────────────────┘
```

### Execution Flow

```
1. WorkloadGenerator     → Generate synthetic workloads
2. ResourceMonitor      → Collect CPU, Memory, Disk metrics
3. FederatedClient      → Train locally on distributed data
4. FederatedServer      → Aggregate client updates (FedAvg)
5. MetricsEvaluator     → Compute performance metrics
6. Dashboard            → Visualize results
```

---

## File Structure

```
federated_cloud_dashboard/
├── app.py                          # Flask entry point (NO training logic)
├── config.py                       # Centralized configuration
├── orchestration.py                # Pipeline coordinator
├── requirements.txt
│
├── federated/
│   ├── __init__.py
│   ├── model.py                    # FederatedNeuralNetwork
│   └── trainer.py                  # FederatedClient, FederatedServer
│
├── simulation/
│   ├── __init__.py
│   ├── workload.py                 # WorkloadGenerator
│   └── resource_monitor.py         # ResourceMonitor
│
├── metrics/
│   ├── __init__.py
│   └── evaluator.py                # MetricsEvaluator
│
├── static/
│   └── style.css                   # Dashboard styling
│
├── templates/
│   └── dashboard.html              # Frontend
│
└── logs/
    └── metrics_log.csv             # Results log
```

---

## Installation

### Requirements
- Python 3.10+
- CPU-only (no GPU/CUDA)
- Localhost demo (127.0.0.1:5000)

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

Visit: `http://127.0.0.1:5000`

---

## Key Components

### 1. WorkloadGenerator (simulation/workload.py)

Generates realistic cloud workload patterns.

```python
from simulation.workload import WorkloadGenerator

gen = WorkloadGenerator(intensity=0.6, random_seed=42)
workloads = gen.generate_batch_workload(num_samples=100)
stats = gen.get_workload_distribution()
```

**Responsibility:** Pure workload generation without side effects.

---

### 2. ResourceMonitor (simulation/resource_monitor.py)

Monitors system resources (CPU, Memory, Disk).

```python
from simulation.resource_monitor import ResourceMonitor

monitor = ResourceMonitor()
metrics = monitor.collect_metrics()  # Single snapshot
avg_metrics = monitor.get_average_metrics(window_size=5)
```

**Responsibility:** System metric collection and averaging.

---

### 3. FederatedNeuralNetwork (federated/model.py)

Simple feedforward neural network for resource optimization.

```python
from federated.model import FederatedNeuralNetwork

model = FederatedNeuralNetwork(input_size=4, output_size=1)
predictions = model.predict(X)
state = model.get_model_state()  # For aggregation
```

**Responsibility:** Model architecture and inference only.

---

### 4. FederatedClient & FederatedServer (federated/trainer.py)

Implements federated learning with FedAvg algorithm.

```python
from federated.trainer import FederatedClient, FederatedServer

client = FederatedClient(client_id=0, model=model)
metrics = client.train_local(X_local, y_local, learning_rate=0.01, epochs=2)
update = client.get_model_update()  # Weights for aggregation

server = FederatedServer(global_model)
agg_info = server.aggregate_models([update1, update2, update3])
```

**Responsibility:** Local training and secure aggregation.

---

### 5. MetricsEvaluator (metrics/evaluator.py)

Computes performance metrics and logs results.

```python
from metrics.evaluator import MetricsEvaluator

evaluator = MetricsEvaluator(log_file='logs/metrics_log.csv')
mse = evaluator.compute_mse(predictions, targets)
r2 = evaluator.compute_r2_score(predictions, targets)
efficiency = evaluator.compute_resource_efficiency(cpu, memory, accuracy)

evaluator.log_metrics_to_csv(metrics_dict)
```

**Responsibility:** Pure metric computation and logging.

---

### 6. FederatedLearningPipeline (orchestration.py)

Orchestrates the entire workflow.

```python
from orchestration import FederatedLearningPipeline

pipeline = FederatedLearningPipeline(num_clients=3, random_seed=42)
results = pipeline.run_simulation(num_rounds=5)
```

**Flow:**
1. Generate synthetic data
2. Distribute to clients (non-IID)
3. Run federated rounds
4. Evaluate metrics
5. Log results

---

## API Endpoints

### `GET /`
Render dashboard page.

### `POST /api/simulation/start`
Start federated learning simulation.

**Response:**
```json
{
  "status": "success",
  "data": {
    "num_rounds": 5,
    "num_clients": 3,
    "final_metrics": {
      "avg_loss": 0.245,
      "std_loss": 0.032,
      "min_loss": 0.210,
      "max_loss": 0.289
    }
  }
}
```

### `GET /api/metrics/current`
Get execution summary.

### `GET /api/model/state`
Get current global model weights.

### `GET /health`
Health check.

---

## Configuration

Edit `config.py` for research parameters:

```python
FEDERATED_CONFIG = {
    "num_clients": 3,
    "num_rounds": 5,
    "local_epochs": 2,
    "learning_rate": 0.01,
    "random_seed": 42
}

OPTIMIZATION_WEIGHTS = {
    "energy_efficiency": 0.4,
    "cost_optimization": 0.35,
    "sla_compliance": 0.25
}
```

---

## Testing

Run the test script to verify all components:

```bash
python test_pipeline.py
```

This validates:
- ✅ Model training and inference
- ✅ Federated aggregation
- ✅ Metric computation
- ✅ End-to-end pipeline
- ✅ CSV logging

---

## Research Contributions

1. **Privacy-Preserving Learning**: Only model weights shared, not raw data
2. **Multi-Objective Optimization**: Balances energy, cost, and SLA
3. **Federated Averaging**: Implements FedAvg for heterogeneous data
4. **Resource Awareness**: Monitors and optimizes system utilization

---

## Architectural Rules (STRICT)

✅ **Single Responsibility Principle**: Each file has one purpose
✅ **Layered Architecture**: Clear separation of concerns
✅ **No Flask Outside app.py**: All training in orchestration layer
✅ **Callable Functions**: Every function must be explicitly callable
✅ **Reproducibility**: Fixed seeds, CPU-only execution
✅ **Exam-Ready**: Modular, documented, lightweight code
✅ **No Unused Imports**: Clean, efficient code
✅ **Explicit Returns**: Functions return values, not just print

---

## Debugging & Logs

Check `logs/metrics_log.csv` for training progress:

```csv
timestamp,round,avg_loss,cpu,memory,disk
2026-01-18T10:00:00,1,0.245,42.3,58.1,35.0
2026-01-18T10:01:00,2,0.231,41.8,57.9,35.0
```

---

## FAQ

**Q: Can I use multiple processes?**
A: No, this is CPU-only localhost demo.

**Q: Can I train on real cloud data?**
A: No, simulation uses synthetic data. Modify `generate_synthetic_data()` for your data.

**Q: How do I change the model architecture?**
A: Edit `FederatedNeuralNetwork.__init__()` in `federated/model.py`.

**Q: Can I add DP (Differential Privacy)?**
A: Yes, modify `FederatedServer.aggregate_models()` or use `PRIVACY_CONFIG`.

---

## Author Notes

**For Viva Presentation:**
- Explain layered architecture clearly
- Walk through execution flow (workload → training → metrics)
- Discuss privacy benefits of federated learning
- Show how each function is callable and testable
- Demonstrate reproducibility with fixed seeds

---

## License

Research Project - Educational Use Only
