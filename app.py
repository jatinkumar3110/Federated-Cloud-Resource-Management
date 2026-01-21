"""
Web Orchestration Layer: Flask Application Entry Point
Serves the dashboard and exposes API endpoints for results.

STRICT RULE: No training logic, workload generation, or metric computation here.
This file is ONLY for:
- Flask route definition
- Calling orchestration.py and new modules (experiments, metrics, visualization)
- Returning JSON responses

Called by: User via browser/requests
Calls: orchestration.FederatedLearningPipeline, experiments, metrics, visualization
"""

from flask import Flask, render_template, jsonify, request, send_file
import config
from orchestration import FederatedLearningPipeline
from experiments.scenario_manager import ScenarioManager
from experiments.experiment_runner import ExperimentRunner
from ui.dashboard_controller import DashboardController
from visualization.comparison_plots import ComparisonPlots
from metrics.fairness import FairnessMetrics
from metrics.communication import CommunicationMetrics
from metrics.sustainability import SustainabilityMetrics
from orchestration_nodes import get_nodes_manager
import os
import io

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize global pipeline (created once at startup)
_pipeline = None


def get_pipeline() -> FederatedLearningPipeline:
    """
    Get or create global pipeline instance.
    
    Returns:
        FederatedLearningPipeline instance
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = FederatedLearningPipeline(num_clients=3, random_seed=42)
    return _pipeline


@app.route('/')
def dashboard():
    """
    Render main dashboard page (v3 - Professional Console).
    
    Returns:
        Rendered dashboard_v3.html template (new professional interface)
    """
    return render_template('dashboard_v3.html')


@app.route('/dashboard/v2')
def dashboard_v2():
    """
    Render legacy v2 dashboard page (original interface).
    
    Returns:
        Rendered dashboard.html template (legacy version)
    """
    return render_template('dashboard.html')


@app.route('/api/simulation/start', methods=['POST'])
def start_simulation():
    """
    Start federated learning simulation with optimization parameters.
    
    Request JSON:
        - alpha: float [0, 1] - Energy efficiency weight (default 0.4)
        - beta: float [0, 1] - Resource balance weight (default 0.35)
        - gamma: float [0, 1] - SLA compliance weight (default 0.25)
        - sla_cpu: float [50, 100] - CPU SLA threshold % (default 80)
        - sla_memory: float [50, 100] - Memory SLA threshold % (default 85)
    
    Returns:
        JSON with simulation results including system metrics
    """
    try:
        # Extract optimization parameters from request
        data = request.get_json() or {}
        alpha = float(data.get('alpha', config.OPTIMIZATION_CONFIG['alpha']))
        beta = float(data.get('beta', config.OPTIMIZATION_CONFIG['beta']))
        gamma = float(data.get('gamma', config.OPTIMIZATION_CONFIG['gamma']))
        sla_cpu = float(data.get('sla_cpu', config.OPTIMIZATION_CONFIG['sla_cpu_threshold']))
        sla_memory = float(data.get('sla_memory', config.OPTIMIZATION_CONFIG['sla_memory_threshold']))
        
        # Validate parameters
        if not (0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1):
            return jsonify({
                "status": "error",
                "message": "Alpha, beta, gamma must be in [0, 1]"
            }), 400
        if not (50 <= sla_cpu <= 100 and 50 <= sla_memory <= 100):
            return jsonify({
                "status": "error",
                "message": "SLA thresholds must be in [50, 100]"
            }), 400
        
        # Run simulation with provided parameters
        pipeline = get_pipeline()
        results = pipeline.run_simulation(
            num_rounds=5,
            alpha=alpha,
            beta=beta,
            gamma=gamma,
            sla_cpu=sla_cpu,
            sla_memory=sla_memory
        )
        return jsonify({
            "status": "success",
            "data": results
        }), 200
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid parameter value: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/metrics/current', methods=['GET'])
def get_current_metrics():
    """
    Get current system metrics.
    
    Returns:
        JSON with current metrics
    """
    try:
        pipeline = get_pipeline()
        summary = pipeline.get_execution_summary()
        return jsonify({
            "status": "success",
            "data": summary
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/model/state', methods=['GET'])
def get_model_state():
    """
    Get current global model state.
    
    Returns:
        JSON with serialized model weights
    """
    try:
        pipeline = get_pipeline()
        state = pipeline.get_current_model_state()
        
        # Convert numpy arrays to lists for JSON serialization
        serializable_state = {
            "weights": state["weights"].tolist(),
            "bias": state["bias"].tolist(),
            "input_size": state["input_size"],
            "output_size": state["output_size"]
        }
        
        return jsonify({
            "status": "success",
            "data": serializable_state
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ============================================================================
# NODE CONFIGURATION MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    """
    Get all configured nodes.
    
    Returns:
        JSON with list of nodes
    """
    try:
        manager = get_nodes_manager()
        nodes = manager.get_all_nodes()
        
        return jsonify({
            "status": "success",
            "data": [node.to_dict() for node in nodes],
            "count": len(nodes)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/nodes', methods=['POST'])
def add_node():
    """
    Add a new node configuration.
    
    Request JSON:
        - node_type: str - EDGE_DEVICE, USER_DEVICE, COMPUTE_SERVER, or DATA_CENTER_NODE
        - cpu_cores: int - Number of CPU cores (> 0)
        - memory_gb: float - Memory in GB (> 0)
        - energy_cost_factor: float - Energy multiplier (> 0)
        - sla_threshold: float - SLA target 0-100
        - region: str - "clean", "mixed", or "fossil" (default: "mixed")
    
    Returns:
        JSON with created node
    """
    try:
        data = request.get_json() or {}
        
        # Validate required fields
        required = ['node_type', 'cpu_cores', 'memory_gb', 'energy_cost_factor', 'sla_threshold']
        for field in required:
            if field not in data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400
        
        manager = get_nodes_manager()
        node = manager.add_node(
            node_type=data['node_type'],
            cpu_cores=int(data['cpu_cores']),
            memory_gb=float(data['memory_gb']),
            energy_cost_factor=float(data['energy_cost_factor']),
            sla_threshold=float(data['sla_threshold']),
            region=data.get('region', 'mixed')
        )
        
        return jsonify({
            "status": "success",
            "data": node.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/nodes/<node_id>', methods=['PUT'])
def update_node(node_id):
    """
    Update node configuration.
    
    Request JSON:
        - Any node fields to update (node_type, cpu_cores, memory_gb, etc.)
    
    Returns:
        JSON with updated node
    """
    try:
        data = request.get_json() or {}
        manager = get_nodes_manager()
        
        # Convert numeric fields
        if 'cpu_cores' in data:
            data['cpu_cores'] = int(data['cpu_cores'])
        if 'memory_gb' in data:
            data['memory_gb'] = float(data['memory_gb'])
        if 'energy_cost_factor' in data:
            data['energy_cost_factor'] = float(data['energy_cost_factor'])
        if 'sla_threshold' in data:
            data['sla_threshold'] = float(data['sla_threshold'])
        
        node = manager.update_node(node_id, **data)
        
        return jsonify({
            "status": "success",
            "data": node.to_dict()
        }), 200
    except KeyError:
        return jsonify({
            "status": "error",
            "message": f"Node not found: {node_id}"
        }), 404
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/nodes/<node_id>', methods=['DELETE'])
def delete_node(node_id):
    """
    Delete a node configuration.
    
    Returns:
        JSON with success/failure status
    """
    try:
        manager = get_nodes_manager()
        deleted = manager.delete_node(node_id)
        
        if deleted:
            return jsonify({
                "status": "success",
                "message": f"Node {node_id} deleted"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Node not found: {node_id}"
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/nodes/clear', methods=['POST'])
def clear_nodes():
    """
    Clear all node configurations.
    
    Returns:
        JSON with success status
    """
    try:
        manager = get_nodes_manager()
        manager.clear_all()
        
        return jsonify({
            "status": "success",
            "message": "All nodes cleared"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/dashboard/metadata', methods=['GET'])
def get_dashboard_metadata():
    """
    Get dashboard metadata (node types, strategies, defaults).
    
    Returns:
        JSON with available node types, strategies, and default parameters
    """
    try:
        controller = DashboardController()
        metadata = controller.get_dashboard_metadata()
        return jsonify({
            "status": "success",
            "data": metadata
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/experiments/scenarios', methods=['GET'])
def get_available_scenarios():
    """
    Get list of available experiment scenarios.
    
    Returns:
        JSON with scenario names and descriptions
    """
    try:
        scenarios = ScenarioManager.list_standard_scenarios()
        scenario_list = []
        for name in scenarios:
            scenario = ScenarioManager.get_standard_scenario(name)
            scenario_list.append({
                "name": name,
                "display_name": scenario.name,
                "description": scenario.description,
                "num_rounds": scenario.num_rounds,
                "num_nodes": sum(scenario.num_nodes_per_type.values()),
                "strategies": scenario.strategies,
            })
        
        return jsonify({
            "status": "success",
            "data": scenario_list
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/experiments/run', methods=['POST'])
def run_experiment():
    """
    Run a single experiment scenario.
    
    Request JSON:
        - scenario_name: str - Name of scenario to run (e.g., "small_scale")
        - export_csv: bool - Whether to export results to CSV (default False)
    
    Returns:
        JSON with experiment results
    """
    try:
        data = request.get_json() or {}
        scenario_name = data.get('scenario_name', 'small_scale')
        export_csv = data.get('export_csv', False)
        
        # Load scenario
        scenario = ScenarioManager.get_standard_scenario(scenario_name)
        
        # Run experiment
        runner = ExperimentRunner(verbose=False)
        csv_file = None
        if export_csv:
            os.makedirs('experiment_results', exist_ok=True)
            csv_file = f"experiment_results/{scenario_name}_{int(__import__('time').time())}.csv"
        
        results = runner.run_experiment(scenario, output_file=csv_file)
        
        # Format results for JSON
        formatted_results = {}
        for strategy, metrics in results.items():
            formatted_results[strategy] = {
                "total_energy": float(metrics['total_energy']),
                "avg_energy": float(metrics['avg_energy']),
                "energy_std": float(metrics['energy_std']),
                "sla_violations": int(metrics['total_sla_violations']),
                "fairness_score": float(metrics['fairness_score']),
                "communication_mb": float(metrics['communication_bytes'] / (1024*1024)),
                "green_score": float(metrics['green_score']),
            }
        
        return jsonify({
            "status": "success",
            "scenario": scenario_name,
            "data": formatted_results,
            "csv_file": csv_file if export_csv else None
        }), 200
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Unknown scenario: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/simulations/run', methods=['POST'])
def run_custom_simulation():
    """
    Run a custom simulation with user-defined nodes.
    
    Request JSON:
        - strategy: str - "Static Allocation", "Federated Learning", "Centralized ML", or "Energy-Aware Heuristic"
        - rounds: int - Number of rounds (default: 5)
        - alpha: float - Energy weight (default: 0.4)
        - beta: float - Fairness weight (default: 0.35)
        - gamma: float - Communication weight (default: 0.25)
    
    Uses nodes configured via /api/nodes endpoints.
    
    Returns:
        JSON with simulation results and visualization paths
    """
    try:
        data = request.get_json() or {}
        
        # Get configured nodes
        manager = get_nodes_manager()
        nodes_list = manager.get_all_nodes()
        
        if not nodes_list:
            return jsonify({
                "status": "error",
                "message": "No nodes configured. Please add nodes via /api/nodes endpoints first."
            }), 400
        
        # Convert to Node objects
        nodes = manager.to_nodes()
        
        # Get simulation parameters
        strategy = data.get('strategy', 'Federated Learning')
        num_rounds = int(data.get('rounds', 5))
        alpha = float(data.get('alpha', 0.4))
        beta = float(data.get('beta', 0.35))
        gamma = float(data.get('gamma', 0.25))
        
        # Validate strategy
        valid_strategies = [
            "Static Allocation",
            "Centralized ML",
            "Federated Learning",
            "Energy-Aware Heuristic"
        ]
        if strategy not in valid_strategies:
            return jsonify({
                "status": "error",
                "message": f"Invalid strategy: {strategy}. Must be one of {valid_strategies}"
            }), 400
        
        # Create dynamic scenario
        from experiments.scenario_manager import Scenario
        
        scenario = Scenario(
            name=f"custom_{len(nodes)}nodes",
            description=f"Custom simulation with {len(nodes)} user-defined nodes",
            num_rounds=num_rounds,
            num_nodes_per_type={},  # Not used for custom nodes
            strategies=[strategy],
            custom_nodes=nodes,
            alpha=alpha,
            beta=beta,
            gamma=gamma
        )
        
        # Run experiment
        runner = ExperimentRunner(verbose=False)
        results = runner.run_experiment(scenario)
        
        # Format results
        formatted_results = {}
        for strat, metrics in results.items():
            formatted_results[strat] = {
                "total_energy": float(metrics['total_energy']),
                "avg_energy": float(metrics['avg_energy']),
                "energy_std": float(metrics['energy_std']),
                "sla_violations": int(metrics['total_sla_violations']),
                "fairness_score": float(metrics['fairness_score']),
                "communication_mb": float(metrics['communication_bytes'] / (1024*1024)),
                "green_score": float(metrics['green_score']),
            }
        
        # Generate visualization
        plots = ComparisonPlots()
        
        visualization_paths = {
            "energy_plot": None,
            "sla_plot": None,
            "fairness_plot": None,
            "dashboard_plot": None
        }
        
        try:
            os.makedirs("temp_plots", exist_ok=True)
            
            # Energy plot
            energy_fig = plots.plot_energy_comparison(results)
            if energy_fig:
                energy_path = "temp_plots/custom_energy.png"
                energy_fig.savefig(energy_path, dpi=100, bbox_inches='tight')
                visualization_paths["energy_plot"] = energy_path
                import matplotlib.pyplot as plt
                plt.close(energy_fig)
            
            # SLA plot
            sla_fig = plots.plot_sla_comparison(results)
            if sla_fig:
                sla_path = "temp_plots/custom_sla.png"
                sla_fig.savefig(sla_path, dpi=100, bbox_inches='tight')
                visualization_paths["sla_plot"] = sla_path
                import matplotlib.pyplot as plt
                plt.close(sla_fig)
            
            # Fairness plot
            fairness_fig = plots.plot_fairness_heatmap(results)
            if fairness_fig:
                fairness_path = "temp_plots/custom_fairness.png"
                fairness_fig.savefig(fairness_path, dpi=100, bbox_inches='tight')
                visualization_paths["fairness_plot"] = fairness_path
                import matplotlib.pyplot as plt
                plt.close(fairness_fig)
            
            # Dashboard plot
            dashboard_fig = plots.plot_multi_metric_dashboard(results)
            if dashboard_fig:
                dashboard_path = "temp_plots/custom_dashboard.png"
                dashboard_fig.savefig(dashboard_path, dpi=100, bbox_inches='tight')
                visualization_paths["dashboard_plot"] = dashboard_path
                import matplotlib.pyplot as plt
                plt.close(dashboard_fig)
        except Exception as vis_error:
            # Visualization is optional, don't fail the whole response
            pass
        
        return jsonify({
            "status": "success",
            "simulation": {
                "strategy": strategy,
                "num_nodes": len(nodes),
                "num_rounds": num_rounds,
                "parameters": {
                    "alpha": alpha,
                    "beta": beta,
                    "gamma": gamma
                }
            },
            "results": formatted_results,
            "visualizations": visualization_paths
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/metrics/fairness', methods=['POST'])
def compute_fairness():
    """
    Compute fairness metrics for nodes.
    
    Request JSON:
        - node_allocations: dict - Node ID to allocation percentage
    
    Returns:
        JSON with fairness metrics
    """
    try:
        data = request.get_json() or {}
        allocations = data.get('node_allocations', {})
        
        if not allocations:
            return jsonify({
                "status": "error",
                "message": "node_allocations required"
            }), 400
        
        # Convert to float array
        alloc_values = [float(v) for v in allocations.values()]
        
        # Compute metrics
        jain = FairnessMetrics.compute_jain_index(alloc_values)
        gini = FairnessMetrics.compute_gini_coefficient(alloc_values)
        gap = FairnessMetrics.compute_allocation_gap(alloc_values)
        cv = FairnessMetrics.compute_coefficient_of_variation(alloc_values)
        
        return jsonify({
            "status": "success",
            "data": {
                "jain_index": float(jain),
                "gini_coefficient": float(gini),
                "allocation_gap": float(gap),
                "coefficient_of_variation": float(cv),
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/metrics/communication', methods=['POST'])
def compute_communication():
    """
    Compute communication overhead metrics.
    
    Request JSON:
        - num_nodes: int - Number of nodes
        - num_rounds: int - Number of federated rounds
        - model_size_bytes: int - Model size in bytes (default 512)
    
    Returns:
        JSON with communication metrics
    """
    try:
        data = request.get_json() or {}
        num_nodes = int(data.get('num_nodes', 4))
        num_rounds = int(data.get('num_rounds', 5))
        model_size = int(data.get('model_size_bytes', 512))
        
        if num_nodes <= 0 or num_rounds <= 0:
            return jsonify({
                "status": "error",
                "message": "num_nodes and num_rounds must be positive"
            }), 400
        
        # Compute metrics
        per_round = (num_nodes * 2 + 1) * model_size  # Simplified calculation
        total = per_round * num_rounds
        redundancy = (2 * num_nodes + 1) * num_rounds
        
        return jsonify({
            "status": "success",
            "data": {
                "per_round_bytes": float(per_round),
                "total_bytes": float(total),
                "total_megabytes": float(total / (1024*1024)),
                "redundancy_factor": float(redundancy),
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/metrics/sustainability', methods=['POST'])
def compute_sustainability():
    """
    Compute sustainability metrics.
    
    Request JSON:
        - total_energy: float - Total energy units consumed
        - region: str - Carbon intensity region ("clean", "mixed", "fossil")
    
    Returns:
        JSON with sustainability metrics
    """
    try:
        data = request.get_json() or {}
        total_energy = float(data.get('total_energy', 0))
        region = data.get('region', 'mixed')
        
        if region not in ['clean', 'mixed', 'fossil']:
            region = 'mixed'
        
        # Convert to kWh and compute carbon
        kwh = total_energy * 0.001
        
        carbon_intensities = {
            "clean": 0.1,
            "mixed": 0.5,
            "fossil": 0.9
        }
        carbon = kwh * carbon_intensities[region]
        
        # Simple green score
        green_score = max(0, 1.0 - (carbon / 10.0))
        
        return jsonify({
            "status": "success",
            "data": {
                "total_energy_kwh": float(kwh),
                "carbon_kg": float(carbon),
                "region": region,
                "green_score": float(green_score),
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint including new modules.
    
    Returns:
        JSON with server status and available features
    """
    return jsonify({
        "status": "healthy",
        "service": "Federated Cloud Dashboard v2",
        "features": {
            "optimization": True,
            "heterogeneous_nodes": True,
            "multiple_strategies": True,
            "fairness_metrics": True,
            "communication_metrics": True,
            "sustainability_metrics": True,
            "visualizations": True,
            "experiment_automation": True,
        }
    }), 200


if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )
