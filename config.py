"""
Configuration Module
Centralized configuration for research-grade project.

Constraints:
- CPU-only execution
- Localhost demo (127.0.0.1)
- Reproducible experiments (fixed seeds)
- Research parameters for federated learning
"""

import os

# ============================================================================
# FLASK CONFIGURATION
# ============================================================================
# Production-safe defaults are used unless explicitly overridden by environment
# variables. For local development, set FLASK_DEBUG=true.
DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() in ('1', 'true', 'yes', 'on')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))

# ============================================================================
# FEDERATED LEARNING CONFIGURATION
# ============================================================================
FEDERATED_CONFIG = {
    "num_clients": 3,              # Number of federated clients
    "num_rounds": 5,               # Federated rounds
    "local_epochs": 2,             # Local training epochs per client
    "learning_rate": 0.01,         # Learning rate for SGD
    "batch_size": 32,              # Batch size for training
    "input_features": 4,           # [cpu, memory, disk, workload]
    "output_dimension": 1,         # Regression output
    "random_seed": 42              # For reproducibility
}

# ============================================================================
# SIMULATION CONFIGURATION
# ============================================================================
SIMULATION_CONFIG = {
    "workload_intensity": 0.6,     # Base workload intensity
    "workload_variance": 0.2,      # Variance factor
    "monitor_interval": 5,         # Seconds between monitoring
    "num_data_samples": 200,       # Synthetic data samples
    "random_seed": 42
}

# ============================================================================
# OPTIMIZATION SCORE CONFIGURATION (NEW - Version 2.0)
# ============================================================================
# Define the learning target as a system optimization score
# optimization_score = α*energy + β*imbalance + γ*sla_penalty
# The model learns to minimize this score, not predict raw metrics

OPTIMIZATION_CONFIG = {
    "alpha": 0.4,                  # Weight for energy consumption (40%)
    "beta": 0.35,                  # Weight for resource imbalance (35%)
    "gamma": 0.25,                 # Weight for SLA penalty (25%)
    "sla_cpu_threshold": 80.0,     # CPU threshold for SLA (%)
    "sla_memory_threshold": 85.0,  # Memory threshold for SLA (%)
}

# ============================================================================
# NORMALIZATION CONFIGURATION
# ============================================================================
# All resource metrics normalized to [0, 1] for stable training

NORMALIZATION_BOUNDS = {
    "cpu_max": 100.0,              # CPU normalized by 100%
    "memory_max": 100.0,           # Memory normalized by 100%
    "disk_max": 100.0,             # Disk normalized by 100%
    "workload_max": 1.0,           # Workload normalized to [0,1]
}

# ============================================================================
# METRICS & LOGGING CONFIGURATION
# ============================================================================
LOG_FILE = 'logs/metrics_log.csv'
LOG_LEVEL = 'INFO'

# ============================================================================
# RESEARCH PARAMETERS
# ============================================================================
# Multi-objective Optimization Weights
OPTIMIZATION_WEIGHTS = {
    "energy_efficiency": 0.4,      # 40% weight on energy
    "cost_optimization": 0.35,     # 35% weight on cost
    "sla_compliance": 0.25         # 25% weight on SLA
}

# SLA Thresholds
SLA_THRESHOLDS = {
    "response_time_max": 1.0,      # Max 1 second
    "cpu_max": 80.0,               # Max 80% CPU
    "memory_max": 85.0             # Max 85% memory
}

# ============================================================================
# PRIVACY CONFIGURATION
# ============================================================================
PRIVACY_CONFIG = {
    "enable_differential_privacy": False,  # For future enhancement
    "epsilon": 1.0,                        # DP budget
    "delta": 1e-5,                         # DP parameter
    "secure_aggregation": False            # For future enhancement
}

# ============================================================================
# VALIDATION
# ============================================================================
def validate_config():
    """Validate configuration parameters."""
    assert FEDERATED_CONFIG["num_clients"] > 0, "num_clients must be positive"
    assert FEDERATED_CONFIG["learning_rate"] > 0, "learning_rate must be positive"
    assert 0 <= OPTIMIZATION_WEIGHTS["energy_efficiency"] <= 1
    assert 0 <= OPTIMIZATION_WEIGHTS["cost_optimization"] <= 1
    assert 0 <= OPTIMIZATION_WEIGHTS["sla_compliance"] <= 1
    
    # Weights should sum approximately to 1
    total_weight = sum(OPTIMIZATION_WEIGHTS.values())
    assert 0.99 <= total_weight <= 1.01, "Optimization weights must sum to 1"


# Validate on import
validate_config()
