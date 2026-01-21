#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick Start Guide - Run Federated Learning Simulation Locally
"""

if __name__ == '__main__':
    import sys
    import io
    
    # Fix Unicode encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    from orchestration import FederatedLearningPipeline
    
    print("\n" + "="*60)
    print("FEDERATED LEARNING - QUICK START")
    print("="*60 + "\n")
    
    print("Starting federated learning simulation...\n")
    
    # Initialize pipeline
    pipeline = FederatedLearningPipeline(num_clients=3, random_seed=42)
    print("[OK] Pipeline initialized with 3 clients\n")
    
    # Run simulation
    print("[RUN] Generating synthetic data...")
    X, y = pipeline.generate_synthetic_data(num_samples=200)
    print(f"[OK] Data generated: {X.shape}\n")
    
    print("[RUN] Distributing data to clients...")
    client_data = pipeline.distribute_data_to_clients(X, y)
    print(f"[OK] Data distributed to {len(client_data)} clients\n")
    
    print("[RUN] Running 5 federated learning rounds...\n")
    
    for round_num in range(1, 6):
        print(f"  --- Round {round_num} ---")
        result = pipeline.run_federated_round(client_data, learning_rate=0.01, epochs=2)
        print(f"      Loss: {result['avg_client_loss']:.4e}\n")
    
    print("\n" + "="*60)
    print("SIMULATION COMPLETE")
    print("="*60 + "\n")
    
    summary = pipeline.get_execution_summary()
    print("Final Metrics:")
    print(f"  - Total Rounds: {summary['total_rounds']}")
    print(f"  - Final Loss: {summary['max_loss']:.4e}")
    print(f"  - CSV Logged: logs/metrics_log.csv")
    print("\n[OK] Open http://127.0.0.1:5000 in your browser to see results\n")
    print(f"Max Loss: {summary['max_loss']:.6f}")
    print(f"Avg CPU Usage: {summary['avg_cpu']:.1f}%")
    print(f"Avg Memory Usage: {summary['avg_memory']:.1f}%")
    print("="*60)
    
    print("\n✓ Simulation complete! Check logs/metrics_log.csv for details.\n")
