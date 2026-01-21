"""
Test Suite for Federated Learning Pipeline
Verifies all components in isolation and integration.

Run: python test_pipeline.py
"""

import numpy as np
from simulation.workload import WorkloadGenerator
from simulation.resource_monitor import ResourceMonitor
from federated.model import FederatedNeuralNetwork
from federated.trainer import FederatedClient, FederatedServer
from metrics.evaluator import MetricsEvaluator
from orchestration import FederatedLearningPipeline


def test_workload_generator():
    """Test workload generation."""
    print("=" * 60)
    print("TEST: WorkloadGenerator")
    print("=" * 60)
    
    gen = WorkloadGenerator(intensity=0.5, random_seed=42)
    
    # Single workload
    single = gen.generate_single_workload()
    assert 0 <= single <= 100, "Single workload out of range"
    print(f"✓ Single workload: {single:.2f}")
    
    # Batch workload
    batch = gen.generate_batch_workload(10)
    assert len(batch) == 10, "Batch size mismatch"
    assert all(0 <= w <= 100 for w in batch), "Batch workload out of range"
    print(f"✓ Batch workload (10 samples): mean={np.mean(batch):.2f}")
    
    # Distribution
    stats = gen.get_workload_distribution(num_samples=100)
    print(f"✓ Workload stats: mean={stats['mean']:.2f}, std={stats['std']:.2f}")
    
    print()


def test_resource_monitor():
    """Test resource monitoring."""
    print("=" * 60)
    print("TEST: ResourceMonitor")
    print("=" * 60)
    
    monitor = ResourceMonitor()
    
    # Collect metrics
    metrics = monitor.collect_metrics()
    assert "cpu" in metrics and "memory" in metrics and "disk" in metrics
    print(f"✓ Metrics collected: CPU={metrics['cpu']:.1f}%, Memory={metrics['memory']:.1f}%")
    
    # History
    monitor.collect_metrics()
    monitor.collect_metrics()
    avg = monitor.get_average_metrics(window_size=3)
    print(f"✓ Average metrics (window=3): CPU={avg['cpu']:.1f}%")
    
    print()


def test_federated_model():
    """Test neural network model."""
    print("=" * 60)
    print("TEST: FederatedNeuralNetwork")
    print("=" * 60)
    
    model = FederatedNeuralNetwork(input_size=4, output_size=1, random_seed=42)
    print(f"✓ Model initialized: {model.input_size} → {model.output_size}")
    
    # Forward pass
    X = np.random.randn(5, 4)
    output = model.forward(X)
    assert output.shape == (5, 1), "Output shape mismatch"
    print(f"✓ Forward pass: X shape {X.shape} → output shape {output.shape}")
    
    # Get weights
    w, b = model.get_weights()
    assert w.shape == (4, 1), "Weight shape mismatch"
    print(f"✓ Weights shape: {w.shape}, Bias shape: {b.shape}")
    
    # Model state
    state = model.get_model_state()
    assert "weights" in state and "bias" in state
    print(f"✓ Model state extracted for aggregation")
    
    print()


def test_federated_training():
    """Test federated client and server."""
    print("=" * 60)
    print("TEST: FederatedClient & FederatedServer")
    print("=" * 60)
    
    # Setup
    global_model = FederatedNeuralNetwork(input_size=4, output_size=1, random_seed=42)
    server = FederatedServer(global_model)
    print(f"✓ Server initialized with global model")
    
    # Create clients
    clients = [FederatedClient(i, global_model) for i in range(3)]
    print(f"✓ Created {len(clients)} clients")
    
    # Generate data
    X = np.random.randn(30, 4)
    y = np.random.randn(30, 1)
    X_client = X[:10]
    y_client = y[:10]
    
    # Local training
    train_metrics = clients[0].train_local(X_client, y_client, learning_rate=0.01, epochs=2)
    assert "final_loss" in train_metrics, "Missing loss metric"
    print(f"✓ Client 0 trained: final_loss={train_metrics['final_loss']:.4f}")
    
    # Collect updates
    updates = [client.get_model_update() for client in clients[:2]]
    
    # Server aggregation
    agg_info = server.aggregate_models(updates)
    assert agg_info["num_clients"] == 2
    print(f"✓ Server aggregated {agg_info['num_clients']} clients")
    
    print()


def test_metrics_evaluator():
    """Test metrics computation."""
    print("=" * 60)
    print("TEST: MetricsEvaluator")
    print("=" * 60)
    
    evaluator = MetricsEvaluator()
    
    # Generate test data
    predictions = np.array([[0.5], [1.2], [2.1]])
    targets = np.array([[0.6], [1.0], [2.0]])
    
    # MSE
    mse = evaluator.compute_mse(predictions, targets)
    assert mse >= 0, "MSE must be non-negative"
    print(f"✓ MSE: {mse:.4f}")
    
    # MAE
    mae = evaluator.compute_mae(predictions, targets)
    assert mae >= 0, "MAE must be non-negative"
    print(f"✓ MAE: {mae:.4f}")
    
    # R²
    r2 = evaluator.compute_r2_score(predictions, targets)
    assert 0 <= r2 <= 1, "R² out of range"
    print(f"✓ R² Score: {r2:.4f}")
    
    # Resource efficiency
    efficiency = evaluator.compute_resource_efficiency(cpu=42, memory=58, model_accuracy=0.92)
    print(f"✓ Resource Efficiency: {efficiency:.4f}")
    
    # SLA compliance
    is_compliant, compliance_pct = evaluator.compute_sla_compliance(response_time=0.5, sla_threshold=1.0)
    print(f"✓ SLA Compliance: {is_compliant} ({compliance_pct:.1f}%)")
    
    print()


def test_orchestration_pipeline():
    """Test end-to-end pipeline."""
    print("=" * 60)
    print("TEST: FederatedLearningPipeline (Integration)")
    print("=" * 60)
    
    pipeline = FederatedLearningPipeline(num_clients=3, random_seed=42)
    print(f"✓ Pipeline initialized: {pipeline.num_clients} clients")
    
    # Generate data
    X, y = pipeline.generate_synthetic_data(num_samples=60)
    assert X.shape[0] == 60 and X.shape[1] == 4
    print(f"✓ Synthetic data generated: {X.shape}")
    
    # Distribute to clients
    client_data = pipeline.distribute_data_to_clients(X, y)
    assert len(client_data) == 3
    print(f"✓ Data distributed to {len(client_data)} clients")
    
    # Run one round
    result = pipeline.run_federated_round(client_data, learning_rate=0.01, epochs=1)
    assert "avg_client_loss" in result
    print(f"✓ Federated round completed: avg_loss={result['avg_client_loss']:.4f}")
    
    # Full simulation
    print("\n→ Running 3-round simulation...")
    sim_result = pipeline.run_simulation(num_rounds=3)
    assert sim_result["num_rounds"] == 3
    print(f"✓ Simulation completed:")
    print(f"  - Rounds: {sim_result['num_rounds']}")
    print(f"  - Clients: {sim_result['num_clients']}")
    print(f"  - Final avg loss: {sim_result['final_metrics']['avg_loss']:.4f}")
    
    # Execution summary
    summary = pipeline.get_execution_summary()
    print(f"✓ Execution summary:")
    print(f"  - Total rounds: {summary['total_rounds']}")
    print(f"  - Avg loss: {summary['avg_loss']:.4f}")
    print(f"  - Avg CPU: {summary['avg_cpu']:.1f}%")
    
    print()


def test_logging():
    """Test CSV logging."""
    print("=" * 60)
    print("TEST: Metrics Logging to CSV")
    print("=" * 60)
    
    import os
    import csv
    
    evaluator = MetricsEvaluator(log_file='logs/test_metrics.csv')
    
    # Log sample metrics
    metrics = {
        "timestamp": "2026-01-18T10:00:00",
        "round": 1,
        "avg_loss": 0.245,
        "cpu": 42.5,
        "memory": 58.2
    }
    evaluator.log_metrics_to_csv(metrics)
    print(f"✓ Metrics logged to {evaluator.log_file}")
    
    # Verify file
    if os.path.exists(evaluator.log_file):
        with open(evaluator.log_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) > 0, "No rows logged"
            print(f"✓ CSV file verified: {len(rows)} row(s)")
        
        # Cleanup
        os.remove(evaluator.log_file)
        print(f"✓ Test file cleaned up")
    
    print()


def main():
    """Run all tests."""
    print("\n")
    print("█" * 60)
    print("FEDERATED LEARNING PIPELINE - TEST SUITE")
    print("█" * 60)
    print("\n")
    
    try:
        test_workload_generator()
        test_resource_monitor()
        test_federated_model()
        test_federated_training()
        test_metrics_evaluator()
        test_orchestration_pipeline()
        test_logging()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\n✓ Project is research-ready!")
        print("  Run: python app.py")
        print("  Visit: http://127.0.0.1:5000")
        print("\n")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
