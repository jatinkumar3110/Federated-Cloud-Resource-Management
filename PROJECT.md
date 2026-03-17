# Federated Cloud Dashboard: Technical Master Document

## 1. Document Purpose

This is the master technical document for the Federated Cloud Dashboard project.

It is written for readers who are completely new to the project and need to understand:

- what the system is,
- why it exists,
- how it works internally,
- how to run it,
- how to deploy it,
- how to secure and operate it,
- how to extend it for research and production.

This document is intentionally exhaustive and can be used as:

- onboarding material,
- architecture reference,
- API handbook,
- operations runbook,
- deployment checklist,
- troubleshooting guide.

---

## 2. Project in One Sentence

A research-grade Flask web platform that simulates federated learning strategies on heterogeneous cloud nodes, evaluates energy/fairness/convergence/carbon trade-offs, and visualizes results through an interactive dashboard with role-based access control.

---

## 3. Problem Statement

Modern cloud environments must optimize multiple conflicting objectives:

- performance,
- energy consumption,
- fairness across nodes/users,
- communication overhead,
- carbon footprint,
- SLA compliance.

Traditional centralized approaches either:

- require moving all data to one location (privacy + bandwidth concerns), or
- ignore sustainability and fairness dimensions.

The project addresses this gap by:

- modeling federated and non-federated strategies,
- generating realistic simulation metrics,
- offering reproducible comparison workflows,
- enabling interactive analysis via web UI.

---

## 3.5 Federated Learning Refresher (For New Readers)

If you are familiar with federated learning, skip to Section 4. Otherwise, read this quick primer.

### What is Federated Learning?

Traditionally, machine learning works like this:

1. Collect all data in one central location (data center).
2. Train a model on that pooled data.
3. Deploy the trained model.

Federated learning flips this:

1. Training data stays distributed across many devices (edge devices, organizations, regions).
2. Each device trains a model locally on its own data.
3. Devices periodically send **model updates** (not raw data) to a central server.
4. The server aggregates the updates (e.g., averaging weights) to produce a global model.
5. The server sends the updated global model back to devices.
6. Repeat for multiple rounds until convergence.

**Key insight**: Data never leaves the device. Only statistical summaries (gradients, weights) are communicated. This preserves privacy and reduces transmission of sensitive information.

### Why Federated Learning Matters

**Privacy**: Raw user data (e.g., medical records, financial transactions, personal messages) remain local and never touch a central server.

**Communication Efficiency**: In IoT and edge scenarios, sending raw data is prohibitively expensive. Sending model updates is orders of magnitude smaller.

**Compliance**: Many regulations (GDPR, HIPAA, CCPA) restrict centralizing personal data. Federated learning can satisfy these requirements.

**Localization**: Models can adapt to local conditions. A keyboard prediction model trained federally can learn local slang and language patterns.

### Challenges Federated Learning Introduces

Unlike centralized training, federated learning introduces new complications:

1. **Heterogeneity**: Devices vary wildly in CPU, memory, network speed, and local data characteristics. A phone != a data center node.
   - How do you ensure slow/weak devices don't lag behind fast ones?
   - This is the **fairness problem**.

2. **Communication Overhead**: Sending model updates 100+ times per round across thousands of devices exhausts bandwidth and energy.
   - How many rounds can we afford? How frequently should we communicate?
   - This is the **communication efficiency problem**.

3. **Convergence**: Will the globally aggregated model actually improve, or will local drift cause divergence?
   - Some aggregation strategies (e.g., simple averaging) converge. Others don't.
   - This is the **convergence problem**.

4. **Energy Consumption**: Edge devices run on batteries. Running neural network training drains them quickly.
   - Can we train with fewer rounds? Fewer computations per round? Smaller models?
   - This is the **energy sustainability problem**.

### Federated Averaging (FedAvg) Algorithm

The most common federated learning algorithm is **FedAvg** (McMahan et al., Google). Here's the pseudocode:

```
On server:
  Initialize global model weights w
  FOR round = 1 to T:
    Sample a fraction of devices
    Send current weights w to sampled devices
    
    FOR each device in parallel:
      Download weights w
      Train locally for E epochs (or K minibatches)
      Compute weight update delta
      Send delta back to server
    
    Server aggregates (averages) all deltas
    Update global weights: w_new = average(all deltas)
```

**Why averaging works**: Each device contributes equally to the next version of the global model, ensuring no single device dominates. This works well when all devices have similar data distributions. When distributions are skewed (one device has biased data), fairness degrades.

### Strategies This Project Simulates

This project doesn't implement full FL training (that would require a deep learning framework). Instead, it simulates realistic metrics that would emerge from different strategies:

1. **Static Allocation** (baseline): No optimization. Devices always work at fixed capacity.
2. **Centralized ML**: Ignore federated constraints. Pretend all data is centralized, then distribute results. Unrealistic, high privacy risk, but best convergence.
3. **Federated Learning (FedAvg-like)**: Standard averaging. Good fairness, moderate communication, good convergence.
4. **Energy-Aware Heuristic**: Automatically reduce rounds, batch sizes, or model precision for low-energy devices. Slower convergence, but lower energy and carbon.

The simulation engine (`simulation_data_generator.py`) encodes realistic profiles for each strategy, allowing researchers to explore tradeoffs without weeks of wall-clock training time.

---

### Functional Goals

1. Configure heterogeneous nodes dynamically.
2. Run transient simulations for fast exploration.
3. Execute persistent experiments for comparison and reproducibility.
4. Display rich visual analytics and per-round behavior.
5. Export and inspect results/logs.

### Research Goals

1. Evaluate strategy trade-offs.
2. Quantify fairness and sustainability impact.
3. Produce paper-ready visual evidence.
4. Maintain deterministic/reproducible behavior where possible.

### Platform Goals

1. Keep architecture modular and extendable.
2. Separate orchestration from model logic.
3. Make cloud deployment straightforward (Render-ready).

---

## 5. High-Level Architecture

### 5.0 Architecture Philosophy

The system is organized into **strict, independent layers**, each with a single responsibility and clean interfaces. This design provides:

1. **Modularity**: Each layer can be tested, modified, or replaced independently.
2. **Testability**: Logic in one layer can be unit-tested without requiring the entire stack.
3. **Scalability**: Heavy simulation computation can be moved to separate workers/services without affecting the web layer.
4. **Maintainability**: Future developers can understand and modify any layer without needing to understand all others.
5. **Research Flexibility**: Researchers can swap simulation engines, strategies, or metrics without touching authentication or web infrastructure.

## 5.1 Layered View

```text
+--------------------------------------------------------------+
| Presentation / UI Layer                                      |
| - templates/dashboard_v3.html (interactive console)         |
| - templates/login.html (authentication gate)                 |
| - Client-side JavaScript + Plotly.js visualizations          |
| [Responsibility: User interaction, form handling, charting]  |
+-----------------------------^--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Web API / Orchestration Layer                                |
| - app.py (Flask WSGI app, HTTP routing, auth, RBAC)         |
| - config.py (environment-driven configuration)               |
| [Responsibility: HTTP request/response, session mgmt,       |
|  access control, error responses, JSON serialization]        |
+-----------------------------^--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Coordination / Business Logic Layer                           |
| - orchestration.py (workflow coordination)                   |
| - orchestration_nodes.py (node lifecycle management)         |
| - experiments/scenario_manager.py (scenario definitions)     |
| - experiments/experiment_runner.py (execution orchestration) |
| [Responsibility: translating user intent into simulations,   |
|  managing node lifecycle, persisting experiment state]        |
+-----------------------------^--------------------------------+
                              |
                              v
+--------------------------------------------------------------+
| Simulation + Science Layer                                   |
| - simulation_data_generator.py (realistic metric engine)     |
| - simulation/*.py (node simulation, workload models)         |
| - metrics/*.py (evaluation: fairness, energy, etc)           |
| - federated/*.py (FL-specific algorithms)                    |
| [Responsibility: physics/statistical realism, accurate       |
|  metrics, research-grade data generation]                    |
+--------------------------------------------------------------+
```

### 5.1a Data Flow Through Layers

A typical user interaction flows through the layers as follows:

1. **User -> UI Layer**: User configures nodes (browser form) and submits to run simulation.
2. **UI -> API Layer**: JavaScript sends `POST /api/simulations/run` with strategy/config.
3. **API -> Coordination**: `app.py` validates request, checks auth/RBAC, then calls `orchestration.run_simulation()`.
4. **Coordination -> Science**: `orchestration.py` instantiates nodes, initializes strategy, then calls `simulation_data_generator.generate_rounds()`.
5. **Science -> Metrics**: `simulation_data_generator.py` produces round-by-round metrics, then `metrics/` modules calculate aggregates (fairness, energy, carbon).
6. **Science -> Coordination**: Metrics result returned to orchestrator.
7. **Coordination -> API**: Result wrapped in JSON.
8. **API -> UI**: JSON response sent to browser.
9. **UI Layer**: JavaScript receives metrics and re-renders all charts via Plotly.js.

Each layer **only knows about the layer directly below it**—not lower layers. This enforces separation and prevents tangled dependencies.

## 5.2 Control Flow Modes

The application supports two distinct simulation modes, each optimized for different research workflows:

### Mode A: Transient Simulation (Fast Exploration)

- **Endpoint**: `POST /api/simulations/run`
- **Purpose**: Instant, interactive exploration of strategy behavior for hypothesis testing and quick comparisons.
- **Persistence**: Results are **not stored**; returned immediately to the client and discarded after session.
- **Typical Users**: All authenticated users (team members + admin).
- **Use Case Example**: "What happens if I increase the number of rounds from 5 to 10?" → Run transient, observe charts, iterate.
- **Response Time**: ~100-150 ms for typical config (10-15 nodes, 10 rounds).
- **Memory Footprint**: Minimal; garbage-collected after response sent.

### Mode B: Persistent Experiment (Reproducible Research)

- **Endpoint**: `POST /api/experiments/execute`
- **Purpose**: Save, version, and compare multiple runs to establish reproducible research artifacts.
- **Persistence**: Results stored in in-memory experiment store (`_experiments` dict) with metadata (name, timestamp, config).
- **Access**: Admin only (RBAC enforced in `before_request()`).
- **Use Case Example**: "I want to test Federated Learning vs Centralized across 5 configurations" → Execute 5 times, each stored. Then compare via `/api/experiments/list` and download CSVs.
- **Response Time**: Slightly above transient due to storage overhead.
- **Durability Note**: Experiments persist across API restarts but are cleared on application restart. For production research, migrate to persistent DB (see Section 18.2).

---

## 6. Repository Structure (Major Components)

```text
.
├── app.py
├── config.py
├── orchestration.py
├── orchestration_nodes.py
├── simulation_data_generator.py
├── requirements.txt
├── render.yaml
├── Procfile
├── templates/
│   ├── dashboard_v3.html
│   ├── dashboard.html
│   └── login.html
├── static/
├── federated/
│   ├── model.py
│   └── trainer.py
├── simulation/
│   ├── node.py
│   ├── node_types.py
│   ├── workload.py
│   └── resource_monitor.py
├── metrics/
│   ├── evaluator.py
│   ├── fairness.py
│   ├── communication.py
│   └── sustainability.py
├── visualization/
│   ├── plot_generator.py
│   └── comparison_plots.py
├── experiments/
│   ├── scenario_manager.py
│   └── experiment_runner.py
├── logs/
│   ├── metrics_log.csv
│   └── user_sessions_log.csv
└── documentation_images/
```

---

## 7. Detailed Module Guide

This section explains what each major module does, why it's structured that way, and how it interacts with its neighbors.

## 7.0 Module Interaction Map

Before diving into details, here's how modules call each other:

```
app.py (HTTP entry)
  |
  +---> orchestration.py ("How do I run this request?")
         |
         +---> orchestration_nodes.py ("What nodes exist?")
         |
         +---> simulation_data_generator.py ("Generate realistic metrics")
         |
         +---> federated/trainer.py ("Run FL aggregation logic")
         |
         +---> metrics/*.py ("Calculate fairness, energy, etc.")
              |
              +---> visualization/plot_generator.py (optional, for export)
              |
              +---> experiments/experiment_runner.py (persist if Mode B)
```

Each arrow represents a module calling a function from another module. Critically, **each module is ignorant of layers above it**—`simulation_data_generator.py` does not import `app.py` or know about HTTP. This enforces clean boundaries.

## 7.0a orchestration.py (Workflow Orchestrator)

**What it does**: The "conductor" of simulations. Takes high-level user intent ("run simulation with Federated strategy for 10 rounds") and coordinates all lower layers to execute it.

**Why separate orchestration from web layer**: Web layer (`app.py`) handles HTTP parsing and auth. Orchestration handles business logic. This separation means:
- Orchestration logic can be tested without spinning up a Flask app or making HTTP requests.
- The same orchestration logic can be called from CLI scripts, notebooks, or background workers.
- Web routes become thin wrappers: parse HTTP -> validate -> call orchestration -> serialize response.

**Key responsibilities**:

1. **Workflow Coordination**: 
   - Accept simulation config (strategy, rounds, node list).
   - Instantiate simulation engine with that config.
   - Call `simulation_data_generator.py` repeatedly to generate round-by-round metrics.
   - Aggregate round results into final summary.
   - Return structured result to caller.

2. **Strategy Initialization**:
   - Given strategy name ("Federated Learning", "Energy-Aware", etc.), instantiate the appropriate strategy object.
   - Set strategy-specific hyperparameters (convergence speed, fairness weighting, etc.).
   - This decoupling allows new strategies to be added without touching `app.py`.

3. **Node Assignment**:
   - Fetch current configured nodes from `orchestration_nodes.py`.
   - Validate that requested nodes exist.
   - Optionally filter or sample nodes if scenario requests a subset.
   - Pass node list to simulation engine.

4. **Error Handling**:
   - If nodes don't exist: return 400 Bad Request with clear message.
   - If strategy unknown: return 400 Bad Request.
   - If simulation crashes: catch exception, log, return 500 Internal Server Error.
   - Never let exceptions bubble up uncaught to `app.py`.

5. **Result Packaging**:
   - Wrap raw metrics in a response envelope: `{"status": "success", "type": "transient", "final_metrics": {...}, "round_results": [...]}`.
   - Ensure all numeric values are JSON-serializable (no NaN, Inf, complex numbers).

**Example flow** (pseudocode):

```python
def run_simulation(strategy_name, rounds, node_ids=None):
    # 1. Validate inputs
    if strategy_name not in KNOWN_STRATEGIES:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    
    # 2. Fetch nodes
    if node_ids:
        nodes = [orchestration_nodes.get_node(nid) for nid in node_ids]
    else:
        nodes = orchestration_nodes.list_nodes()
    
    if not nodes:
        raise ValueError("No nodes configured")
    
    # 3. Initialize simulation
    strategy = instantiate_strategy(strategy_name)
    sim = SimulationEngine(nodes=nodes, strategy=strategy)
    
    # 4. Run rounds
    round_results = []
    for r in range(rounds):
        metrics = sim.generate_round(r)
        round_results.append(metrics)
    
    # 5. Aggregate
    final_metrics = compute_aggregates(round_results)
    
    # 6. Return
    return {
        "status": "success",
        "final_metrics": final_metrics,
        "round_results": round_results,
    }
```

## 7.0b federated/trainer.py (Federated Aggregation Logic)

**What it does**: Implements federated learning-specific algorithms, primarily weight aggregation (FedAvg and variants).

**Why separate from general simulation**: Not all strategies are federated. Centralized and static strategies use different aggregation logic:
- **Centralized**: No aggregation; all improvements happen at the server.
- **Federated**: Average device weights; all devices contribute equally.
- **Energy-Aware**: Weighted average (low-energy devices weighted higher, high-energy weighted lower).

By isolating FL logic, we can switch aggregation strategies without touching the simulation engine.

**Key concepts**:

1. **Client Model Update**: Each device trains locally, producing a weight delta (gradient).
2. **Server Aggregation**: Server collects deltas from all clients and computes a weighted average.
   - FedAvg: Uniform weights (1/num_clients per client).
   - Weighted FedAvg: Weight by dataset size (larger datasets have more say).
   - Clustered FedAvg: Group similar clients; aggregate within clusters; then aggregate clusters.

3. **Convergence Guarantees**: Mathematical proofs show that FedAvg converges towards global optimum under certain conditions (IID data, fixed learning rate). This project doesn't implement these proofs but respects their implications:
   - Strategy-specific convergence curves are hardcoded to match theoretical expectations.
   - Heterogeneous data (skewed distributions) reduce convergence speed and fairness; this is reflected in metric generation.

**Implementation in this project** (simplified):

```python
def aggregate_client_updates(client_deltas, strategy='fedavg'):
    """
    client_deltas: List of weight updates from each client
    strategy: 'fedavg' (uniform), 'weighted' (by data size), 'energy_aware'
    """
    if strategy == 'fedavg':
        # Simple average
        return sum(client_deltas) / len(client_deltas)
    
    elif strategy == 'weighted':
        # Weighted by dataset size
        total_size = sum(d['size'] for d in client_deltas)
        weighted_sum = sum(d['delta'] * d['size'] / total_size 
                          for d in client_deltas)
        return weighted_sum
    
    elif strategy == 'energy_aware':
        # Low-energy clients weighted higher (less communication cost)
        weights = [1.0 / client_deltas[i]['energy'] 
                  for i in range(len(client_deltas))]
        weights = [w / sum(weights) for w in weights]  # normalize
        return sum(client_deltas[i]['delta'] * weights[i] 
                  for i in range(len(client_deltas)))
```

This simplified aggregation is plugged into the round-by-round simulation to determine convergence trajectory.

## 7.1 app.py (Flask WSGI Application + Request Router)

**What it does**: Acts as the entry point for all HTTP requests. Handles routing, session management, authentication, role-based access control, and error responses.

**Why this design**: Flask is a lightweight web framework that doesn't dictate project structure. By keeping `app.py` primarily as a router (not business logic), we keep the web layer thin and testable.

**Key responsibilities**:

1. **Route Registration**: Maps HTTP paths to handler functions (e.g., `GET / -> dashboard`, `POST /api/simulations/run -> run_simulation`).
2. **Authentication Gate**: Global `before_request()` middleware checks session cookies. If no session exists, return 401 unless the path is public (login, logout, health, static files).
3. **Role-Based Access Control (RBAC)**: For sensitive endpoints (admin-only), checks `session['role'] == 'admin'`. If not, returns 403 Forbidden.
4. **Session Management**: Uses Flask's session object (server-side storage) to track logged-in users. Session dict contains `username`, `role`, and `login_at` timestamp.
5. **Password Verification**: On login form POST, hashes incoming password with `werkzeug.security.check_password_hash()` against stored hashes from `USER_ACCOUNTS` dict.
6. **Activity Logging**: Calls `log_user_activity(event, details)` to record each API call, failure, or state change to `logs/user_sessions_log.csv`.
7. **Error Response Serialization**: Catches exceptions and returns JSON error responses with appropriate HTTP status codes (400 Bad Request, 401 Unauthorized, 500 Server Error, etc.).
8. **Orchestration Delegation**: For complex workflows, calls functions in `orchestration.py` and wraps results in JSON responses.

**Code patterns to know**:
- Session access: `session['username']`, `session['role']`
- Protected routes: decorated with `@require_login` or checked in handler
- Admin-only routes: checked via `is_admin()` helper function
- Error responses: `return jsonify({'error': '...'}), 403`

**Not in app.py** (intentionally): Heavy simulation logic, data generation algorithms, metric calculations—those live in lower layers.

## 7.1a Authentication Deep-Dive

The login flow is straightforward but security-conscious:

```python
USER_ACCOUNTS = {
    'admin': (hash('admin_password'), 'admin'),
    'mugdhi': (hash('mugdhi_password'), 'user'),
    ...
}

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in USER_ACCOUNTS:
        stored_hash, role = USER_ACCOUNTS[username]
        if check_password_hash(stored_hash, password):
            session['username'] = username
            session['role'] = role
            session['login_at'] = datetime.now().isoformat()
            log_user_activity('login_success', f'user={username}')
            return redirect('/')
    
    log_user_activity('login_failed', f'user={username}')
    return render_template('login.html', error='Invalid credentials')
```

Key security points:
- Passwords are **never stored in plaintext**; only hashes are in the code.
- In production, passwords come from environment variables: `os.getenv('ADMIN_PASSWORD')`.
- Failed login attempts are logged and can be monitored for brute-force attacks.
- Session tokens are opaque and server-side; users cannot forge session IDs.

## 7.2 config.py (Centralized Configuration)

**What it does**: Centralizes all tunable parameters and runtime settings in one place, making the application easy to reconfigure without code changes.

**Why this design**: Configuration should be separate from code for two reasons: (1) production deployments often change settings (debug mode, database URLs, API keys) without code changes, (2) it's easier to understand what the system's knobs are if they're all in one file.

**Key settings**:

1. **Flask Config**: `DEBUG`, `HOST`, `PORT`, `SECRET_KEY`
   - `DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() in ('true', '1')`
   - Production must have `DEBUG=false` to prevent stack trace leaks and enable optimizations.
2. **Federated Defaults**: `NUM_ROUNDS`, `LEARNING_RATE`, aggregation method
   - These affect baseline behavior when users don't override.
3. **Simulation Bounds**: Min/max energy per node, fairness range, carbon intensity by region
   - Used by `simulation_data_generator.py` to constrain generated metrics to realistic ranges.
4. **Strategy-Specific Weights**: For each strategy (Federated, Centralized, etc.), hardcoded convergence speed, fairness weighting
   - Allows researchers to tune how different strategies behave without code edits.
5. **Metric Norms**: What is "good" fairness, energy, carbon? Used for score calculations.
   - Example: `FAIRNESS_NORM = 0.85` means fairness scores ≥ 0.85 are considered good.

**Production adaptations**:
- All sensitive values (database URLs, API keys, passwords) read from environment variables via `os.getenv('KEY', 'default')`.
- This allows deployment platforms (Render, AWS, Docker) to inject secrets without changing code.
- Local development can use a `.env` file (via `python-dotenv`) if desired, but `.env` should **not** be committed to Git.

## 7.3 simulation_data_generator.py (Realistic Simulation Engine)

**What it does**: The core research engine. Generates realistic, research-grade metrics for federated learning simulations based on strategy choice, node configuration, and round count.

**Why this design**: Traditional ML frameworks (TensorFlow, PyTorch) train models on real data but are heavy and data-dependent. This project instead generates plausible metrics using statistical and physical models, allowing researchers to explore strategy tradeoffs without real data. This is more like a **test-bed** than a real ML system.

**Key simulation components**:

### Energy Model (Per-Node, Per-Round)

Physical energy consumption depends on CPU utilization, node type, and power profile:

\[
E_{node} = P_{base}(type) \times (0.3 + 0.7 \times u_{cpu}) \times \frac{cores}{8}
\]

where:
- $P_{base}(type)$ = baseline power draw (e.g., edge device = 10W, data-center = 500W)
- $u_{cpu}$ = CPU utilization in [0, 1] (strategy-dependent; federated tasks lighter than centralized)
- $cores/8$ = normalize power to 8-core reference machine

**Why this formula**: Real devices have a baseline idling power and scale sublinearly with load (10% load ≠ 10% energy). The 0.3-0.7 coefficients capture this non-linear behavior.

### Communication Overhead Model

Model weights and gradients transmitted per round, multiplied by network cost per byte:

\[
Comm_{round} = 2 \times \sum_{nodes} overhead(type)
\]

where $2\times$ accounts for uplink (client -> server) and downlink (server -> client).

**Why duplicated**: In federated learning, clients upload gradients to the server, server aggregates, then broadcasts the updated global model back. Hence the factor of 2.

### Convergence Model (Learning Progress)

How quickly the model improves as rounds increase. Uses exponential decay (asymptotic convergence):

\[
conv(r) = s + (1 - s) \times e^{-d \times r}
\]

where:
- $s$ = asymptotic convergence (e.g., 0.85 = best possible accuracy is 85%)
- $d$ = decay rate (e.g., 0.3 = fast convergence, 0.05 = slow convergence)
- $r$ = round index (1, 2, ..., num_rounds)

**Why exponential**: Real ML training exhibits diminishing returns. Early rounds improve rapidly; later rounds improve slowly. Exponential decay captures this curve accurately.

**Strategy-specific profiles**:
- **Static Allocation**: Low convergence speed ($s=0.65, d=0.05$), simulates poor strategy choice.
- **Centralized**: High initial speed but plateaus early ($s=0.80, d=0.20$), simulates overtraining on central data.
- **Federated Learning**: Balanced ($s=0.82, d=0.12$), simulates generalization from diverse nodes.
- **Energy-Aware**: Slower but better fairness tradeoff ($s=0.78, d=0.08$).

### Carbon Footprint Model

Embodied carbon from energy consumption, weighted by regional grid carbon intensity:

\[
CO_2(kg) = Energy(kWh) \times CarbonIntensity_{region}(kg/kWh)
\]

Examples:
- Clean region (e.g., Nordic): 50 gCO2/kWh
- Mixed region (e.g., Europe avg): 250 gCO2/kWh
- Fossil region (e.g., coal-heavy): 800 gCO2/kWh

**Why this matters for research**: Sustainability-aware strategy selection is a growing research area. This model quantifies the carbon benefit of energy-efficient federated approaches.

### Fairness Model

Heterogeneous devices in federated learning can experience different convergence speeds and energy costs. Fairness measures whether slower/weaker nodes are left behind:

\[
Fairness = 1 - Variance(per-node\_convergence) / NormalizationFactor
\]

**Why variance-based**: High variance means some nodes converge well, others lag. Federated averaging (FedAvg) typically produces more balanced convergence across diverse nodes than centralized training.

**Strategy behaviors**:
- **Centralized**: Lower fairness (server optimizes for its own data, clients' local models diverge).
- **Federated**: Higher fairness (explicit averaging ensures all nodes have equal say).

### Data Validation / Guard Rails

Before returning metrics, `simulation_data_generator.py` applies sanity checks:

```python
assert 0 <= fairness_score <= 1.0, f"Fairness out of range: {fairness_score}"
assert energy >= 0, f"Negative energy: {energy}"
assert not math.isnan(convergence), "NaN in convergence"
assert not math.isinf(carbon), "Inf in carbon"
```

If any metric violates constraints, the simulation fails loudly with a clear error, not silently returning garbage data. This is critical for research integrity.

## 7.4 orchestration_nodes.py (Node Lifecycle Management)

**What it does**: Manages the collection of nodes (virtual federated learning clients) that users configure to define their simulation scenario.

**Why this design**: Nodes are stateful (users add/remove/modify them between simulations). Rather than scattering node data across multiple files, we centralize node management here. It acts like a simple database.

**Key responsibilities**:

1. **Node CRUD** (Create, Read, Update, Delete):
   - `add_node(node_id, type, cores, memory, energy_cost, sla_threshold, region)`: Register a new node.
   - `get_node(node_id)`: Retrieve node config.
   - `list_nodes()`: Return all currently configured nodes.
   - `update_node(node_id, **updates)`: Modify node properties.
   - `delete_node(node_id)`: Remove a node (admin-only).
   - `clear_all_nodes()`: Reset to empty slate (admin-only).

2. **Node Validation**:
   - Ensure `cores` is positive, `memory` > 0, `energy_cost` > 0.
   - Check that `region` is in allowed set ("clean", "mixed", "fossil").
   - Reject invalid `type` (must be in predefined list: "edge", "compute", "storage").

3. **Node Presets**: Convenience functions for rapid setup:
   - `preset_sample_cluster()`: Create 5 diverse nodes (edge + compute + mixed regions) for initial testing.
   - `preset_heterogeneous_fleet()`: 12-node cluster simulating real-world diversity.
   - Users can select presets via the UI; they call this module to populate nodes.

4. **Storage**: Nodes stored in a module-level dict `_configured_nodes`. Not persistent (cleared on restart), but persists across simulation runs in the same session.

## 7.5 experiments package (Experiment Tracking)

### scenario_manager.py

**What it does**: Defines and manages experimental scenarios. A scenario is a template: "Run strategy X with Y nodes and Z rounds."

**Key concepts**:
- Scenarios are JSON-serializable (required for REST API).
- Each scenario specifies: strategy name, round count, node list, and hyperparameters (alpha, beta, gamma weights).
- Researchers can define scenarios programmatically (useful for batch runs) or interactively via the dashboard UI.

**Example scenario**:
```json
{
  "name": "Heterogeneous Federated",
  "strategy": "Federated Learning",
  "num_rounds": 20,
  "nodes": ["edge-1", "compute-3", ...],
  "weights": {
    "alpha": 0.4,
    "beta": 0.35,
    "gamma": 0.25
  }
}
```

### experiment_runner.py

**What it does**: Takes a scenario and executes it against one or more strategies, collecting results.

**Key logic**:
1. Loop over selected strategies.
2. For each strategy, instantiate the simulation with scenario config.
3. Collect round-by-round metrics.
4. Aggregate into summary statistics (mean, max, min, std dev).
5. Store result in the experiment store (in-memory dict) with a unique ID.
6. Optionally export to CSV.

**Example usage** (admin endpoint):
```
POST /api/experiments/execute
Body: {"name": "Q1 Study", "strategy": "Federated Learning", "rounds": 15}
Response: {"experiment_id": 42, "status": "success", ...}
```

Users can then retrieve the result via:
```
GET /api/experiments/42
Response: Detailed metrics, round table, summary stats
```

## 7.6 metrics package (Research Metric Evaluation)

**What it does**: Computes domain-specific metrics that researchers care about, given raw simulation output.

**Why separate from simulation**: Simulation generates round-by-round numbers (energy, convergence, etc.). Metrics interpret those numbers:
- Is 0.72 convergence good? (Depends on strategy baseline.)
- How fair is 0.85? (Depends on diversity of nodes.)
- Is 50 MB communication acceptable? (Depends on bandwidth constraints.)

By separating simulation (data generation) from metrics (interpretation), we can:
- Change metric definitions without re-running simulations.
- Compute new metrics on old simulation data.
- Make research hypotheses explicit (e.g., "we consider fairness ≥ 0.85 as excellent").

### evaluator.py

Computes summary statistics and performance scores:
- Average, stddev, min, max of all per-round metrics.
- Composite "performance score" weighted by alpha/beta/gamma.

### fairness.py

Measures heterogeneity impact:
- Per-node convergence variance.
- SLA violation count (fraction of nodes missing latency/accuracy targets).
- Gini coefficient (wealth-inequality metric) adapted for model accuracy distribution.

### communication.py

Analyzes bandwidth utilization:
- Total MB transmitted across all rounds.
- Peak round communication (useful for bandwidth provisioning).
- Compression potential (estimates data reduction if compression applied).

### sustainability.py

Quantifies environmental impact:
- Total energy (kWh).
- Total carbon footprint (kg CO2 eq).
- Regional decomposition (how much comes from clean vs fossil regions).
- "Green score": composite metric incentivizing energy + carbon reduction.

## 7.7 visualization package (Rich Analytics Export)

**What it does**: Renders simulation/experiment results into static plots (PNG, PDF) for research papers and reports.

### plot_generator.py

Wrapper around Matplotlib with server-friendly defaults:
- Uses Agg backend (non-GUI) for headless deployment.
- Helper functions: `plot_convergence()`, `plot_energy()`, `plot_fairness_heatmap()`.
- Returns PNG bytes (no file I/O, safe for web).

### comparison_plots.py

Comparative visualization across multiple experiments:
- Side-by-side strategy comparison (bar charts, box plots).
- Pareto frontier plots (e.g., energy vs fairness tradeoffs).
- Time-series overlays (convergence curves across strategies).

**Why separated into visualization package**: Charts are generated on-demand from REST endpoints, not baked into HTML. Allows users to export charts in various formats (PNG, SVG, PDF) directly from dashboard.

---

## 8. Frontend System (dashboard_v3.html) - Interactive Research Console

**Design Philosophy**: The dashboard is not a pretty consumer app. It's a **research console**—it prioritizes:
- **Completeness**: Show all relevant metrics and controls, even if it means complexity.
- **Interactivity**: Let researchers explore data dynamically without page reloads.
- **Comparison**: Multiple side-by-side views for strategy comparison.
- **Export**: Support data download and chart imaging for papers.

The dashboard achieves this through a modular, sectioned interface where each section owns a domain of functionality.

### 8.1 Architecture of dashboard_v3.html

The HTML structure is organized into collapsible sections:

```
Dashboard
├─ Header (with current user, role, logout button)
├─ Navigation Tabs
│  ├─ Overview
│  ├─ Node Configuration
│  ├─ Strategies
│  ├─ Federated Analytics
│  ├─ Fairness & Carbon
│  ├─ Experiments
│  ├─ Compare Sims
│  ├─ Logs & Export (admin-only)
│  └─ About
└─ Footer
```

Each tab is a `<div id="tab-name">` that shows/hides via JavaScript. Switching tabs is instant (no server round-trip).

### 8.2 Major UI sections (What Researchers Do Here)

#### **Overview Tab**
Entry point. Shows:
- Last simulation result summary (KPIs: energy, fairness, convergence, carbon).
- Quick preset buttons ("Sample 5 Nodes", "Heterogeneous Fleet").
- Quick action buttons ("Run Simulation", "Execute Experiment").

**User goal**: Get an overview of current state and jump to the action they want.

#### **Node Configuration Tab**
Manage the federated cluster:
- Text input fields to add nodes (type, cores, memory, region, energy cost).
- Table listing all configured nodes with delete buttons (admin-only).
- Clear-all button (admin-only).
- Preset buttons to populate with standard node sets.

**User goal**: Define the "devices" in the federated system. Different node configs lead to different convergence and fairness curves.

#### **Strategies Tab**
Choose and compare:
- Dropdown list of available strategies (Static, Centralized, Federated, Energy-Aware).
- For each strategy, a card showing:
  - Strategy description.
  - Quick-run button ("Run with 10 rounds").
  - Hyperparameter sliders (alpha, beta, gamma weights).
  - Strategy-specific info (why convergence differs, where it's best used).

**User goal**: Quickly switch between strategies and understand their differences. Run transient simulations to explore behavior.

#### **Federated Analytics Tab**
Rich visualizations of simulation results:
- **Convergence Curves**: Line chart showing accuracy over rounds. Overlaid if multiple strategies recently run.
- **Energy Heatmap**: Grouped bar chart of per-node energy consumption.
- **Clients Chart**: Box plot or scatter of per-client convergence variance.
- **Communication Trend**: Line chart of cumulative MB transmitted per round.
- **Metrics Box Plots**: Fairness, convergence spread across rounds.
- **ROC/PR Curves** (advanced): Model quality evaluation (rarely used in non-classification scenarios but included for completeness).
- **Histogram**: Distribution of per-node metrics (energy, convergence).
- **Radar Chart**: Multi-dimensional strategy comparison (energy, fairness, convergence, communication, sustainability).

**User goal**: Understand simulation behavior in detail. Spot anomalies, confirm hypotheses, export charts for papers.

#### **Fairness & Carbon Tab**
Focus on sustainability and equity:
- **Fairness Score**: Major KPI, visualized as progress bar and number.
- **SLA Violations**: Count and detailed table of nodes missing targets.
- **Carbon Breakdown**: Pie chart of CO2 by region (clean/mixed/fossil).
- **Green Score**: Composite metric balancing energy, carbon, and fairness.
- **Energy by Node Type**: Stacked bar (edge, compute, storage contributions).

**User goal**: Demonstrate compliance with fairness/sustainability constraints. Support papers on green federated learning.

#### **Experiments Tab** (Admin-Only)
Manage persistent experiment data:
- Text input to name and create a new experiment.
- Table listing all saved experiments (name, timestamp, strategy, final metrics).
- Buttons to load, compare, and delete experiments.
- Export to CSV button.

**User goal**: Store multiple runs side-by-side for reproducibility. Compare experiment series (e.g., 5 runs of FedAvg with different configs).

#### **Compare Sims Tab**
Comparative analytics:
- Dropdown list of recent simulations to select for comparison.
- Side-by-side tables of metrics.
- Overlaid line charts (convergence curves, energy trends).
- Difference highlights (what's better in Strategy A vs B).

**User goal**: Make evidence-based strategy choices. Quantify tradeoffs ("FedAvg has 5% better fairness but 10% more communication.").

#### **Logs & Export Tab** (Admin-Only)
Operational insights:
- **Session Logs**: Table of user activities (login, API calls, denials), timestamp, IP, user agent.
- **Metrics Log**: Optional; raw per-round data export to CSV.
- **Export Buttons**: Download all data as JSON (for processing in Python).

**User goal**: Audit who accessed the system, troubleshoot issues, export data for offline analysis.

#### **About Tab**
Documentation embedded in the UI:
- Project description.
- Quick reference to key metrics (convergence, fairness, etc.) and what they mean.
- Link to PROJECT.md for detailed docs.

**User goal**: Onboard new users without leaving the dashboard.

### 8.3 UX Patterns & Interactions

#### **Real-Time Chart Updates**
When a simulation completes:
1. JavaScript receives JSON response with metrics.
2. For each chart, call the corresponding `draw*()` function (e.g., `drawConvergenceCurve()`).
3. Plotly.js re-renders the chart with new data.
4. No page refresh needed.

**Why this matters**: Users see feedback immediately. They can quickly iterate (change config, run again, observe).

#### **Chart Expand / Fullscreen**
Every chart has an expand button (visible on hover):
1. Click expands chart to full viewport.
2. User can interact with Plotly modebar (zoom, pan, export PNG).
3. Click again or press `Esc` to return to normal view.

**Why this matters**: For presentations and papers, users need high-quality chart exports. Fullscreen mode makes detailed inspection easy.

#### **Modebar (Hover-Visible Tools)**
Plotly charts ship with a toolbar (home, zoom, pan, export). It's hidden by default for clean appearance but shows on chart hover.

**Why this matters**: Researchers are comfortable with Plotly; they expect these tools. Hidden default keeps the UI clean.

#### **Role-Based Control Hiding**
JavaScript function `applyRolePermissions()` runs on page load:
```javascript
if (user.role !== 'admin') {
    document.querySelectorAll('.admin-only').forEach(el => {
        el.style.display = 'none';
    });
}
```

Admin-only elements (node delete button, experiments list, session logs) have class `admin-only`. Non-admins don't see them.

**Why this matters**: Prevents confusion and accidental clicks. Also reinforces the mental model: "some features are not for me."

#### **Preset Buttons**
Quick-start buttons like "Sample 5 Nodes":
1. User clicks button.
2. JavaScript calls `fetch('/api/nodes/preset?name=sample5')`.
3. Nodes added server-side (via orchestration_nodes.py).
4. Dashboard refreshes node list and summary metrics.

**Why this matters**: New users need scaffolding. Presets let them run a meaningful simulation in 2 clicks instead of 10.

#### **Progressive Enhancement**
The dashboard works without JavaScript only for the login gate. The main dashboard **requires** JavaScript because:
- Charts (Plotly.js) are client-side only.
- Real-time updates expect it.
- Tab switching without server calls is expected.

For production internet-facing systems, this would be a risk (JavaScript errors = broken app). For research, it's acceptable because:
- Target audience (researchers, engineers) expects modern web.
- Research focuses on backend logic, not fallback UX.

### 8.4 Data Binding (How Frontend Stays in Sync with Backend)

After each simulation, the server responds with:
```json
{
    "status": "success",
    "final_metrics": {...},
    "round_results": [...],
    "simulation": {...}
}
```

JavaScript stores this in a module-level variable:
```javascript
let lastSimulation = response;  // Global state
```

When user switches tabs, the `draw*()` functions reference `lastSimulation`:
```javascript
function drawConvergenceCurve() {
    const rounds = lastSimulation.round_results.map(r => r.convergence_metric);
    Plotly.newPlot('convergenceChart', [{
        y: rounds,
        type: 'scatter',
        mode: 'lines+markers'
    }]);
}
```

**Why this design**: No need for additional API calls. Frontend caches the last result. When user wants to re-visualize, JavaScript re-renders from cache.

### 8.5 Error Handling in Frontend

When API calls fail (network error, server error, validation error), JavaScript:
1. Catches the error.
2. Displays a sticky error banner at the top: "Error: Failed to run simulation. Check that nodes are configured."
3. Logs the full error to browser console for debugging.
4. Offers a "Retry" button.

**Why this matters**: Users aren't left hanging. They know what went wrong and how to fix it (if fixable).

---

## 9. Authentication, Authorization, Session Model - Security Deep-Dive

## 9.0 Why Auth Matters for This Project

Even though this is research software, not production SaaS, authentication provides:

1. **Audit Trail**: Track who ran which experiments, when, and from where. Critical for research reproducibility and integrity.
2. **Multi-User Isolation**: When multiple researchers use the same instance, prevent one from accidentally (or maliciously) deleting another's work.
3. **Demo / Teaching Readiness**: If you present this to a wider audience, showing role-based controls demonstrates professional software engineering.
4. **Operational Safety**: Admin-only controls prevent junior researchers from accidentally clearing the node list or deleting all experiments.

## 9.1 Account Model - Four Predefined Users

Current configuration:

| Username  | Password Source | Role | Permissions |
|-----------|-----------------|------|-------------|
| admin | `ADMIN_PASSWORD` env var | admin | All endpoints including experiments, node deletion, session logs |
| mugdhi | `MUGDHI_PASSWORD` env var | user | Transient simulations, node creation (read-only), cannot delete nodes or experiments |
| sanya | `SANYA_PASSWORD` env var | user | Transient simulations, node creation (read-only), cannot delete nodes or experiments |
| evaluator | `EVALUATOR_PASSWORD` env var | user | Transient simulations, node creation (read-only), cannot delete nodes or experiments |

**Why these names**: They represent a research team. The admin is the lab lead; the others are team members with limited powers.

**Why environment variables for passwords**: Source code should *never* contain plaintext passwords, even for development. The approach:

```python
ADMIN_PASSWORD_ENV = os.getenv('ADMIN_PASSWORD', 'dev_default_change_me')
admin_hash = generate_password_hash(ADMIN_PASSWORD_ENV)  # Once at startup

USER_ACCOUNTS = {
    'admin': (admin_hash, 'admin'),
    ...
}
```

At deployment (e.g., on Render):
```
ADMIN_PASSWORD=<strong_random_string> \ 
FLASK_SECRET_KEY=<another_strong_string> \
python app.py
```

This way, even if the repository is public, credentials are safe (they live in private deployment config).

## 9.2 Login Flow - Step-by-Step

### User initiates login:

1. User opens app in browser.
2. `before_request()` middleware checks `session['username']`.
3. If missing, middleware redirects to `/login`.
4. Browser displays `templates/login.html` with username/password form.

### User submits credentials:

1. User types username and password, clicks "Sign In".
2. Form POSTs to `app.py` `/login` route:
   ```
   POST /login
   Content-Type: application/x-www-form-urlencoded
   username=admin&password=secret123
   ```

3. `app.py` login handler:
   ```python
   @app.route('/login', methods=['POST'])
   def login():
       username = request.form.get('username')
       password = request.form.get('password')
       
       # 1. Check username exists
       if username not in USER_ACCOUNTS:
           log_user_activity('login_failed', f'user={username}, reason=unknown_user')
           return render_template('login.html', error='Invalid username or password'), 401
       
       # 2. Extract stored hash and role
       stored_hash, role = USER_ACCOUNTS[username]
       
       # 3. Hash incoming password and compare (timing-safe)
       if not check_password_hash(stored_hash, password):
           log_user_activity('login_failed', f'user={username}, reason=wrong_password')
           return render_template('login.html', error='Invalid username or password'), 401
       
       # 4. Credentials valid. Set server-side session.
       session['username'] = username
       session['role'] = role
       session['login_at'] = datetime.now().isoformat()
       
       # 5. Log successful login
       log_user_activity('login_success', f'user={username}, role={role}')
       
       # 6. Redirect to dashboard
       return redirect('/')
   ```

### Session established:

1. Flask internally generates a session ID (random token).
2. Session ID is stored in a signed, encrypted cookie sent to browser.
3. Browser stores cookie.
4. For all subsequent requests, browser automatically includes the cookie.
5. `before_request()` middleware checks the session ID, looks up `session['username']` and `session['role']`, and grants access.

### User logs out:

1. User clicks "Logout" button on dashboard.
2. Clicks POST to `/logout`:
   ```python
   @app.route('/logout')
   def logout():
       username = session.get('username')
       log_user_activity('logout', f'user={username}')
       session.clear()  # Destroy server-side session
       return redirect('/login')
   ```

3. Session cleared.
4. Browser removed the session cookie.
5. User is back at login page.

## 9.3 Access Control - Who Can Do What

### Public Routes (No Login Required)

- `GET /login`: Display login form.
- `POST /login`: Process login.
- `GET /api/health`: Health check for monitoring.
- `GET /static/*`: CSS, JavaScript, images.

### Protected Routes (Login Required)

Any route not listed as public requires `session['username']` to be set. If not, `before_request()` returns 401 Unauthorized.

### Admin-Only Routes (Admin + Login Required)

Certain routes additionally check `session['role'] == 'admin'`:

```python
@app.route('/api/experiments/list')
def list_experiments():
    if not is_admin():
        return jsonify({'error': 'Admin-only endpoint'}), 403
    return jsonify(get_all_experiments())
```

**Admin-only endpoints**:
- `PUT /api/nodes/<id>`: Modify a node.
- `DELETE /api/nodes/<id>`: Delete a node.
- `POST /api/nodes/clear`: Clear all nodes.
- `POST /api/experiments/execute`: Save a persistent experiment.
- `GET /api/experiments/list`: List all saved experiments.
- `GET /api/experiments/<id>`: Fetch experiment detail.
- `DELETE /api/experiments/delete/<id>`: Delete experiment.
- `GET /api/model/state`: Fetch internal model state (sensitive).
- `GET /api/session-logs`: Fetch user activity logs.

### Team Member (Non-Admin) Allowances

Team members (mugdhi, sanya, evaluator) can:
- `POST /api/simulations/run`: Run transient simulations (unlimited).
- `GET /api/nodes`: List configured nodes.
- `POST /api/nodes`: Add new nodes.
- `GET /api/auth/me`: Check current username/role.
- Save nothing persistently (all simulations are ephemeral).

**Rationale**: Team members contribute to research (running sims, testing hypotheses) but don't manage the project state. The admin handles cleanup and archiving.

## 9.4 Session Audit Logging - The Paper Trail

Every login, logout, API call, and access denial is logged to `logs/user_sessions_log.csv`.

**Log structure**:
```csv
timestamp,username,role,event,path,method,ip,user_agent,details
2025-03-17T10:05:32.123456,admin,admin,login_success,,,,ip=192.168.1.1,user-agent=Mozilla/5.0...,
2025-03-17T10:05:45.234567,admin,admin,api_access,/api/nodes,POST,192.168.1.1,Mozilla/5.0...,
2025-03-17T10:06:12.345678,mugdhi,user,api_access,/api/simulations/run,POST,192.168.1.5,Mozilla/5.0...,
2025-03-17T10:06:45.456789,mugdhi,user,denied,/api/experiments/list,GET,192.168.1.5,Mozilla/5.0...,admin-only endpoint
```

**Fields**:
- `timestamp`: ISO-8601 when event occurred.
- `username`: Who performed the action (null for public endpoints).
- `role`: That user's role (admin or user).
- `event`: Type of action (login_success, api_access, denied, etc.).
- `path`: HTTP path (e.g., `/api/nodes`).
- `method`: HTTP method (GET, POST, DELETE).
- `ip`: Client's IP address (useful for detecting attacks).
- `user_agent`: Browser/client identifier.
- `details`: Freeform context (e.g., 'reason=wrong_password' on failed login).

**Logged events**:
- `login_success`: Successful password auth.
- `login_failed`: Wrong password or unknown user.
- `logout`: User clicked logout.
- `api_access`: Any non-denied API call.
- `denied`: Access denied (non-admin tried admin endpoint, or auth failed).

**Why CSV**: Simple, human-readable, tools like Excel can open it. For analytics, pipe it into Python/pandas for deeper investigation.

**Log retention**: Currently unbounded (grows without limit). For production, add a TTL/rotation policy (Section 25).

## 9.5 Session Mechanics - How the Web Forgets You

Flask sessions are **server-side** by default. Here's how it works:

1. User logs in. Flask generates a random `session_id` (e.g., `abc123def456`).
2. Stores session data server-side in memory:
   ```python
   _sessions = {
       'abc123def456': {
           'username': 'admin',
           'role': 'admin',
           'login_at': '2025-03-17T10:05:32.123456'
       }
   }
   ```
3. Sends `session_id` to browser in a signed cookie:
   ```
   Set-Cookie: session=abc123def456; Path=/; HttpOnly; SameSite=Lax
   ```
   The cookie is **signed** (not encrypted) with `FLASK_SECRET_KEY`. Tampering is detected.

4. Browser stores the cookie.
5. For all future requests, browser includes the cookie:
   ```
   Cookie: session=abc123def456
   ```
6. `before_request()` verifies the signature and looks up the session ID:
   ```python
   session_id = request.cookies.get('session')
   if session_id in _sessions:
       # Valid session, allow access
   else:
       # Invalid session, return 401
   ```

**Advantages of server-side sessions**:
- Tamper-proof. Clients can't forge or modify session data.
- Revocation-safe. Logout immediately takes effect (session deleted from server).
- Server has full audit trail (all active sessions and their timestamps).

**Disadvantages**:
- Scales poorly across multiple servers (need shared session storage like Redis).
- In-memory storage is lost on restart (for this project, acceptable; for production, use persistent session store).

## 9.6 Password Hashing - Why We Never Store Plain Text

Werkzeug's `generate_password_hash()` uses **PBKDF2** with 1000 iterations:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# At startup
admin_password_plaintext = os.getenv('ADMIN_PASSWORD')
admin_hash = generate_password_hash(admin_password_plaintext)

# admin_hash looks like: 'pbkdf2:sha256:1000$...$...'
# Plaintext is never stored or kept in memory after this.

# At login
incoming_password = request.form.get('password')
if check_password_hash(admin_hash, incoming_password):
    # Password matches
else:
    # Password doesn't match
```

**Why this is secure**:
- If the source code is leaked, passwords are still safe (only hashes leaked, which are one-way).
- `check_password_hash()` is **timing-safe** (takes same time whether password is close to correct or completely wrong), preventing brute-force timing attacks.
- 1000 iterations of PBKDF2 slow down brute-force password guessing.

**What's missing (for production)**: Argon2 (even stronger than PBKDF2), rate limiting on login attempts, password complexity requirements. See Section 14.3.

---

## 10. API Catalog

Below is a functional catalog of major routes.

## 10.1 UI Routes

- `GET /` -> primary dashboard page (`dashboard_v3.html`)
- `GET /dashboard/v2` -> legacy dashboard
- `GET|POST /login` -> authentication
- `GET|POST /logout` -> session clear

## 10.2 Auth/User Context Routes

- `GET /api/auth/me` -> current username + role
- `GET /api/session-logs` -> admin-only activity log retrieval

## 10.3 Core Simulation Routes

- `POST /api/simulation/start`
- `POST /api/simulations/run` (transient)
- `POST /api/simulations/run_old` (backward compatibility)

## 10.4 Node Management Routes

- `GET /api/nodes`
- `POST /api/nodes`
- `PUT /api/nodes/<node_id>` (admin only)
- `DELETE /api/nodes/<node_id>` (admin only)
- `POST /api/nodes/clear` (admin only)

## 10.5 Experiment Routes

- `GET /api/experiments/scenarios`
- `POST /api/experiments/run`
- `POST /api/experiments/execute` (persistent, admin only)
- `GET /api/experiments/list` (admin only)
- `GET /api/experiments/<id>` (admin only)
- `DELETE /api/experiments/delete/<id>` (admin only)

## 10.6 Metrics Routes

- `GET /api/metrics/current`
- `GET /api/model/state` (admin only)
- `POST /api/metrics/fairness`
- `POST /api/metrics/communication`
- `POST /api/metrics/sustainability`

## 10.7 Health Route

- `GET /api/health`

---

## 11. Data Contracts (Representative)

## 11.1 Simulation Request

```json
{
  "strategy": "Federated Learning",
  "rounds": 10,
  "alpha": 0.4,
  "beta": 0.35,
  "gamma": 0.25
}
```

## 11.2 Simulation Response (Representative)

```json
{
  "status": "success",
  "type": "transient_simulation",
  "final_metrics": {
    "avg_energy": 1.54,
    "fairness_score": 0.89,
    "convergence_metric": 0.72,
    "communication_mb": 46.0,
    "carbon_footprint_kg": 1.98,
    "green_score": 0.86,
    "sla_violations": 0
  },
  "round_results": [
    {
      "round": 1,
      "energy_used": 1.65,
      "communication_mb": 46.0,
      "fairness_score": 0.80,
      "convergence_metric": 0.41
    }
  ],
  "num_clients": 12,
  "simulation": {
    "strategy": "Federated Learning",
    "num_nodes": 12,
    "num_rounds": 10
  }
}
```

---

## 12. Logging and Observability

## 12.1 Runtime Logs

- Flask/gunicorn runtime output
- error stack traces
- Render deploy logs (cloud)

## 12.2 Data/Session Logs

- `logs/metrics_log.csv`
- `logs/user_sessions_log.csv`

## 12.3 Recommended Monitoring Additions

1. request timing middleware
2. structured JSON logs
3. exception IDs and correlation IDs
4. log shipping to external sink

---

## 13. Deployment Architecture - Local, Cloud, and Beyond

## 13.0 Deployment Philosophy

The application is designed to be **deployment-agnostic**: 
- Core logic (simulation, metrics, models) doesn't know or care where it runs.
- Configuration is environment-driven (settings read from env variables, not hardcoded).
- The same Python code runs on laptop, cloud server, or container cluster without modification.

Two deployment modes are currently supported:

1. **Local Development** (your machine, instant feedback)
2. **Cloud Production** (Render, publicly accessible)

Future: containerization (Docker), multi-node scaling (Kubernetes), batch job mode (running experiments without web interface).

## 13.1 Local Development Deployment

### Rationale

During development, you want:
- Fast iteration (change code, hit F5, immediate reload)
- Full debug output (stack traces, print statements)
- No credential management overhead
- Ability to inspect and modify in-memory state

### Setup

```bash
# 1. Clone repo
git clone <repo_url>
cd Federated_Cloud_Dashboard

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run app
python app.py
```

### Configuration (Local Defaults)

Local development uses defaults from `config.py`:

```python
DEBUG = True  # Hot reload on code changes
LOG_LEVEL = 'DEBUG'  # Verbose logging
HOST = 'localhost'  # Only local connects
PORT = 5000  # Standard Flask port
FLASK_SECRET_KEY = 'dev_insecure_key_change_in_production'  # Insecure but convenient
```

These are safe for local use because:
- DEBUG=True only accepts localhost connections.
- Secret key exposure only affects you.
- No external users.

### Runtime

Flask's built-in server starts:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Watching for file changes...
```

**Important**: Flask's built-in server is single-threaded and slow. This is fine for 1-2 users (you) but unsuitable for production (see below).

### Accessing the App

1. Open browser to `http://localhost:5000`
2. Login with test credentials (hardcoded defaults in `app.py`):
   - Username: `admin`, Password: `dev_default_change_me`
   - (In production, these are replaced by env vars)
3. Test the simulation pipelines

### Troubleshooting Local Deployment

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**: You didn't activate virtual env or forgot `pip install -r requirements.txt`.
```bash
source .venv/bin/activate  # Activate venv
pip install -r requirements.txt  # Install packages
```

**Problem**: `Address already in use: ('0.0.0.0', 5000)`

**Solution**: Another process is using port 5000. Either:
- Kill it: `lsof -i :5000` (Mac/Linux) or `netstat -ano | findstr :5000` (Windows), then kill.
- Change port: `PORT=5001 python app.py`

**Problem**: Charts not rendering (blank dashboard)

**Solution**: Run a simulation first. The UI waits for data before drawing charts.

## 13.2 Production Deployment (Render Cloud Platform)

### Rationale

For production (team access, long-running, 24/7 availability), you need:
- High-performance WSGI server (not Flask's dev server)
- Auto-restart on crash
- Environment-driven secrets (not hardcoded)
- HTTPS encryption
- Monitoring and logging
- Easy deployment and rollback

Render is chosen because:
- Free tier available for educational/research projects
- Automatic HTTPS
- Simple GitHub integration (deploy on push)
- Built-in monitoring and logs

### Configuration Files

Two files control Render deployment:

#### `render.yaml` (Infrastructure as Code)

```yaml
services:
  - type: web
    name: federated-cloud-dashboard
    runtime: python
    runtimeVersion: 3.11.9
    buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
    healthCheckPath: /api/health
    envVars:
      - key: FLASK_DEBUG
        value: "false"
      - key: PYTHON_VERSION
        value: 3.11.9
      - fromGroup: secrets  # Reference secret group defined in Render dashboard
```

**Explanation**:
- `runtimeVersion: 3.11.9`: Pin exact Python to avoid wheel incompatibility.
- `buildCommand`: Upgrade pip, then install deps. Ensures setuptools/wheel available for wheel builds.
- `startCommand: gunicorn`: Production WSGI server, binds to all interfaces, 2 workers for concurrency, 120-sec timeout for long simulations.
- `healthCheckPath: /api/health`: Render pings this endpoint. If down >3 times, app restarts.

#### `Procfile` (Process Type Definition)

```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

Alternative to gunicorn command line. Some platforms read this instead of render.yaml startCommand.

### Environment Variables (Secrets)

Variables needed at runtime:

| Key | Source | Purpose |
|-----|--------|----------|
| FLASK_SECRET_KEY | Render Secrets (set manually) | Session signing key (64+ hex chars) |
| FLASK_DEBUG | render.yaml (hardcoded `false`) | Disable debug mode |
| ADMIN_PASSWORD | Render Secrets | Admin login password |
| MUGDHI_PASSWORD | Render Secrets | Team member password |
| SANYA_PASSWORD | Render Secrets | Team member password |
| EVALUATOR_PASSWORD | Render Secrets | Team member password |
| HOST | render.yaml (hardcoded `0.0.0.0`) | Bind all interfaces |
| PORT | Render injects at runtime | Render-assigned port (usually 10000+) |

**Setup process**:

1. On Render dashboard, create a "secret group" with these values.
2. In render.yaml, reference it: `fromGroup: secrets`.
3. Render injects them at container startup.

### Deployment Process

1. **Commit and push to GitHub**:
   ```bash
   git add app.py config.py render.yaml Procfile requirements.txt
   git commit -m "Major version: add auth RBAC, Render support"
   git push origin main
   ```

2. **Connect Render to GitHub**:
   - Go to render.com, login, click "Create New" > "Web Service"
   - Select GitHub account and repository
   - Render scans for render.yaml

3. **Configure secrets on Render dashboard**:
   - Click "Environment" tab on service page
   - Add secret group with FLASK_SECRET_KEY, passwords, etc.
   - **Do not paste secrets in code or Git!**

4. **Deploy**:
   - Every git push to main triggers auto-deploy
   - Render clones repo, runs buildCommand, then starts app with startCommand
   - Takes ~2-3 minutes

5. **Monitor**:
   - Render dashboard shows deployment status
   - Click "Logs" to see output
   - Health check endpoint `/api/health` is polled every 30 seconds

### Runtime Behavior on Render

Once deployed:

- **URL**: `https://federated-cloud-dashboard.onrender.com` (auto-assigned HTTPS)
- **Concurrency**: 2 gunicorn workers = up to 2 concurrent requests
- **Memory**: Free tier gets 512 MB RAM
- **Storage**: Ephemeral (data lost on restart)
- **Startup time**: ~30 seconds (from full shutdown to accepting requests)

### Configuration on Render (Production Mode)

Unlike local development, production uses strict settings:

```python
DEBUG = False  # No detailed error pages to attackers
LOG_LEVEL = 'INFO'  # Less verbose (reduces log storage cost)
HOST = '0.0.0.0'  # Accept all incoming connections
PORT = int(os.getenv('PORT', 5000))  # Render injects port
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')  # From Render secrets
SESSION_COOKIE_SECURE = True  # HTTPS-only (Render provides HTTPS)
SESSION_COOKIE_HTTPONLY = True  # No JS access
```

### Troubleshooting Render Deployment

**Problem**: `ModuleNotFoundError` at runtime

**Solution**: Dependency missing from requirements.txt.
```bash
pip install <missing_package>
pip freeze | grep <missing_package>  # Get exact version
echo <missing_package>==<version> >> requirements.txt
git add requirements.txt && git commit -m "Add missing dependency" && git push
```

Render auto-redeploys on push.

**Problem**: Health check fails, app restarts continuously

**Solution**: `/api/health` endpoint crashing. Check Render logs:
```
GET /api/health -> 500 Internal Server Error
```

Fix the endpoint in app.py, push, and redeploy.

**Problem**: App works locally but fails on Render

**Possible causes**:
- Missing dependency (missing from requirements.txt)
- Hardcoded path that doesn't exist on Render (e.g., `C:\Users\...`)
- Matplotlib backend issue (see visualization/plot_generator.py for Agg backend fix)
- Python version difference (should be 3.11.9 on both)

**Fix**: Add debug logging, redeploy, check Render logs.

## 13.3 Gunicorn (WSGI Application Server)

### Why Gunicorn?

Flask is a **web framework**, not a **server**. It provides routing but not:
- Concurrency (handling multiple requests simultaneously)
- Process management (restarting on crash)
- Load balancing (distributing requests)

Gunicorn is a **WSGI server** that wraps Flask and adds these.

### How Gunicorn Works

```
Gunicorn Master Process
├─ Worker 1 (can handle 1 request)
├─ Worker 2 (can handle 1 request)
└─ Load Balancer (routes incoming requests to idle worker)
```

When two requests arrive concurrently:
- Worker 1 handles request A.
- Worker 2 handles request B.
- Request C waits in queue until a worker is free.

Without Gunicorn (only Flask dev server):
- Request A is handled.
- Requests B and C wait, blocking each other.

### Gunicorn Configuration

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

Explanation:
- `app:app`: Module.application entry point (flask app object)
- `--bind 0.0.0.0:$PORT`: Listen on all interfaces, PORT from environment
- `--workers 2`: 2 concurrent processes (appropriate for Render free tier)
- `--timeout 120`: Kill worker if request takes >120 seconds (long simulations)

### Tuning Gunicorn for Your Workload

**Light usage** (1-2 users, no long sims):
```
gunicorn app:app --workers 2 --worker-class sync --timeout 30
```

**Heavy usage** (many concurrent users, long simulations):
```
gunicorn app:app --workers 4 --worker-class gevent --worker-connections 100 --timeout 600
```

For this project (research, light usage), `--workers 2 --timeout 120` is balanced.

## 13.4 Health Check Endpoint

Render periodically calls `GET /api/health` to verify the app is alive:

```python
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200
```

If this endpoint:
- Returns 200: App is healthy, no action.
- Returns error or times out 3 times in a row: Render restarts the app.

Keep the health endpoint lightweight; simulating should not happen here.

## 13.5 Environment Variables - Reference

### Local Development

```bash
# Optional (uses config.py defaults)
export FLASK_DEBUG=true
export FLASK_SECRET_KEY=dev_insecure_for_local_only
export HOST=localhost
export PORT=5000

# For testing auth without relying on hardcoded defaults
export ADMIN_PASSWORD=my_test_password

python app.py
```

### Render Production

Set via Render dashboard (Settings > Environment):

```
FLASK_SECRET_KEY=<64-char-hex-from-openssl-rand-hex-32>
FLASK_DEBUG=false
ADMIN_PASSWORD=<strong_random_string>
MUGDHI_PASSWORD=<strong_random_string>
SANYA_PASSWORD=<strong_random_string>
EVALUATOR_PASSWORD=<strong_random_string>
```

### Typical Values

```bash
# Generate strong keys
FLASK_SECRET_KEY=$(openssl rand -hex 32)  # 64-char hex
ADMIN_PASSWORD=$(openssl rand -base64 16 | tr -d '=+/' | head -c 16)  # 16-char alphanumeric
```

---

## 14. Security Posture - Current State and Hardening Roadmap

## 14.0 Security Maturity Assessment

This project prioritizes **research functionality** over production security. It has **foundational controls** (auth, RBAC, audit logging) but lacks **advanced protections** (rate limiting, CSRF, DDoS mitigation, encryption in transit).

**Current stance**: Safe for internal lab use. Not recommended for internet-facing public deployment without hardening (Section 14.3).

## 14.1 Current Implemented Controls

### 1. Authentication Gate
**What**: All non-public routes require valid session cookie.

**Prevents**: Unauthorized access to experiments, data, and controls.

**Threat Model**:
- ❌ Attacker accesses app with no account
- ✅ Attacker is forced to login first

### 2. Role-Based Access Control (RBAC)
**What**: Admin-only endpoints check `session['role'] == 'admin'`.

**Prevents**: Non-admin users from accessing sensitive operations (deleting experiments, viewing audit logs, modifying nodes).

**Threat Model**:
- ❌ Malicious team member runs `DELETE /api/experiments/delete/all`
- ✅ Request rejected with 403 Forbidden

### 3. Password Hashing
**What**: `werkzeug.security.generate_password_hash()` via PBKDF2-SHA256.

**Prevents**: Plaintext password leaks if source code is compromised.

**Threat Model**:
- ❌ Attacker steals source code repository
- ✅ Only password hashes leaked; plaintext unrecoverable without months of compute

### 4. Session Tokens
**What**: Server-side sessions with signed (not encrypted) cookies.

**Prevents**: Session hijacking and forgery (attacker can't fake a session ID without the signing key).

**Threat Model**:
- ❌ Attacker crafts fake session cookie `session=fake123`
- ✅ Server verifies signature, detects tampering, rejects cookie

### 5. Audit Logging
**What**: All logins, logouts, API calls, and access denials logged to CSV.

**Prevents**: Silent attacks. Any breach leaves a paper trail.

**Threat Model**:
- ❌ Attacker deletes all experiments and logs out without trace
- ✅ CSV audit log captures the deletion and attacker's IP/timestamp

### 6. Timing-Safe Password Checking
**What**: `check_password_hash()` takes constant time regardless of password correctness.

**Prevents**: Timing attacks (attackers deducing correct password length or prefix from response time).

**Threat Model**:
- ❌ Attacker sends 1000 login requests, measuring response times to infer password prefix
- ✅ Response time is constant; no information leaked

## 14.2 Security Gaps and Risks

### Gap 1: No Rate Limiting
**Risk**: Brute-force password guessing.

**Attack scenario**:
```
Attacker runs 1000 login attempts/second:
  POST /login, username=admin, password=try1
  POST /login, username=admin, password=try2
  ...
  POST /login, username=admin, password=correct_password!
```

Since there's no delay, attacker can try billions of passwords in hours. Strong passwords mitigate (admin password should be 16+ chars), but it's not foolproof.

**Current state**: No rate limiting. Expected for lab use (only 4 internal users). High risk for internet-facing.

### Gap 2: No CSRF Protection
**Risk**: Cross-Site Request Forgery on form endpoints.

**Attack scenario**:
1. Admin visits malicious website while logged into the dashboard.
2. Malicious site has hidden form:
   ```html
   <form action="https://dashboard.example.com/api/nodes/clear" method="POST">
     <input name="confirm" value="yes" />
   </form>
   ```
3. JavaScript auto-submits the form using admin's session cookie.
4. All nodes deleted without admin's consent.

**Current state**: No CSRF tokens. Forms are vulnerable. GET requests are safe (idempotent); destructive operations should use POST + CSRF token.

**Mitigation**: Flask-WTF library adds automatic CSRF tokens to forms.

### Gap 3: Plaintext Passwords in Environment Variables
**Risk**: If deployment environment is compromised, passwords leak.

**Attack scenario**:
1. Attacker gains shell access to Render server.
2. Reads environment variables: `ADMIN_PASSWORD=secret123`.
3. Uses password to login as admin.

**Current state**: Intentional trade-off (easier than secrets manager for lab use). Acceptable if deployment is trusted.

**Mitigation**: Use Render's secret storage or external vault (HashiCorp Vault, AWS Secrets Manager).

### Gap 4: No HTTPS / TLS Enforcement
**Risk**: Passwords sent over plain HTTP (if development configuration).

**Attack scenario**:
1. User connects to `http://dashboard.example.com` (unencrypted).
2. Attacker on shared network sniffs password from plaintext HTTP body.

**Current state**: If deployed to Render (HTTPS enforced), this is mitigated. For local development, it's unencrypted (acceptable).

**Mitigation**: Render automatically provides HTTPS. For self-hosted, use reverse proxy (nginx) with Let's Encrypt TLS certificates.

### Gap 5: Session Cookies Not Hardened
**Risk**: Cookies can be stolen via JavaScript’s `document.cookie` if any XSS (cross-site scripting) vulnerability exists.

**Current state**: Cookies are signed but not marked `HttpOnly`. JavaScript can access them if a vulnerability exists.

**Mitigation**: Set `SESSION_COOKIE_HTTPONLY = True` in config.py. Prevents JavaScript access (even if XSS exists, attacker can't read session cookie).

### Gap 6: Unlimited Audit Log Growth
**Risk**: CSV audit log grows without bound, consuming disk space.

**Attack scenario**:
1. Attacker scripts 1000 login attempts/second for a week.
2. CSV grows to 10 GB, exhausting disk storage.
3. App crashes due to write failure.

**Current state**: No log rotation. Acceptable for lab (small activity volume). High risk for production.

**Mitigation**: Add log rotation (e.g., archive to new file daily, compress old files, delete files >90 days old).

### Gap 7: No Input Validation
**Risk**: SQL injection (if DB used) or command injection (if user input used in shell scripts).

**Current state**: In-memory storage (no SQL). User input not used in shell scripts. Low risk currently.

**Mitigation**: If moving to DB, use parameterized queries. Never concatenate user input into shell commands.

### Gap 8: No Intrusion Detection
**Risk**: Repeated failed logins not flagged. Attacker can silently brute-force.

**Attack scenario**: Admin doesn't notice 100K failed login attempts in audit log (no alerting).

**Current state**: No alerting. Log must be manually reviewed.

**Mitigation**: Add monitoring: if >10 failed logins in 1 hour, trigger alert (email, Slack, PagerDuty).

## 14.3 Recommended Hardening Plan (Before Production)

If deploying to the public internet, apply these in order:

### Priority 1: Immediate (Day 1)

1. **Replace default passwords**: Remove fallback hardcoded defaults. Force environment variable (no default).
   ```python
   admin_password = os.getenv('ADMIN_PASSWORD')
   if not admin_password:
       raise ValueError("ADMIN_PASSWORD env var not set. Aborting.")
   ```

2. **Set strong `FLASK_SECRET_KEY`**: Use `openssl rand -hex 32` to generate 64-char key.
   ```bash
   export FLASK_SECRET_KEY=$(openssl rand -hex 32)
   ```

3. **Ensure `FLASK_DEBUG=false` in production**.
   ```python
   if not os.getenv('FLASK_DEBUG', '').lower() in ('true', '1'):
       app.config['DEBUG'] = False
   ```

4. **Enable secure cookies**:
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS-only
   app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JS access
   app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF mitigation
   ```

### Priority 2: Short-term (Week 1)

5. **Add login rate limiting**:
   ```python
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address
   
   limiter = Limiter(
       app=app,
       key_func=get_remote_address,
       default_limits=["200 per day", "50 per hour"]
   )
   
   @app.route('/login', methods=['POST'])
   @limiter.limit("5 per minute")  # Max 5 login attempts/minute
   def login():
       ...
   ```

6. **Add CSRF tokens to forms**:
   ```python
   from flask_wtf.csrf import CSRFProtect
   csrf = CSRFProtect(app)
   
   # In login.html:
   <form method="POST" action="/login">
       {{ csrf_token() }}
       ...
   </form>
   ```

7. **Add response headers (security.py or middleware)**:
   ```python
   @app.after_request
   def set_security_headers(response):
       response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['X-Frame-Options'] = 'DENY'
       response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' cdn.plot.ly"
       return response
   ```

8. **Set up log rotation**:
   ```python
   import logging
   from logging.handlers import RotatingFileHandler
   
   handler = RotatingFileHandler(
       'logs/user_sessions_log.csv',
       maxBytes=10*1024*1024,  # 10 MB
       backupCount=10  # Keep 10 old files
   )
   ```

### Priority 3: Medium-term (Month 1)

9. **Use secrets manager** (Render Secrets or external vault):
   - Remove passthrough environment variables.
   - Store all secrets in Render dashboard.
   - Reference via `FLASK_SECRET_KEY` env var (injected by Render at runtime).

10. **Add request logging middleware** (correlation IDs):
    ```python
    @app.before_request
    def log_request():
        request.correlation_id = str(uuid.uuid4())
        logger.info(f"[{request.correlation_id}] {request.method} {request.path}")
    ```

11. **Set up alerting** for suspicious activity:
    - Webhook to send Slack message on >5 failed logins in 5 minutes.
    - Email admin on DELETE /api/experiments/* calls.

### Priority 4: Long-term (Quarter 1)

12. **Migrate sessions to persistent store** (Redis or PostgreSQL):
    - Current in-memory store is lost on restart.
    - Redis: `pip install flask-session[redis]`
    ```python
    from flask_session import Session
    app.config['SESSION_TYPE'] = 'redis'
    Session(app)
    ```

13. **Add MFA** (multi-factor authentication):
    - `pip install pyotp qrcode`
    - Admin users scan QR code, get 6-digit code generator.
    - Login requires both password and current TOTP code.

14. **Implement audit log archive**:
    - Write logs to cold storage (S3, GCS) for long-term retention.
    - Keep last 30 days in hot storage (local CSV).

15. **Conduct security audit**:
    - Penetration testing by external firm.
    - Dependency scanning (pip audit, Snyk).
    - Code review for injection vulnerabilities.

## 14.4 Security Checklist for Production Deployment

Before going live on the internet, verify all:

- [ ] No plaintext passwords in code or .env file
- [ ] `FLASK_SECRET_KEY` is 64+ random hex characters
- [ ] `FLASK_DEBUG=false` in production config
- [ ] `SESSION_COOKIE_SECURE=true`
- [ ] `SESSION_COOKIE_HTTPONLY=true`
- [ ] HTTPS enforced (Render does this automatically)
- [ ] Login rate limiting enabled (5 attempts/min)
- [ ] CSRF tokens in all POST forms
- [ ] Security headers set (HSTS, X-Frame-Options, etc.)
- [ ] Audit log rotation configured
- [ ] Admin password is 16+ characters, randomly generated
- [ ] Slack/email alerting configured
- [ ] Log retention policy documented
- [ ] Dependency versions pinned in requirements.txt
- [ ] `pip audit` run and all critical CVEs patched
- [ ] Third-party security scan (Snyk, Black Duck) passed

---

## 15. Performance Characteristics

Observed ranges (typical local runs):

- transient simulation: ~100-150 ms
- experiment list/get: tens of ms
- persistent execution: slightly above transient due to storage path

Performance drivers:

1. number of nodes
2. number of rounds
3. number of active charts/DOM updates
4. serialization payload size

---

## 16. Testing and Validation Strategy - Ensuring Quality

## 16.0 Testing Philosophy

This project prioritizes **functional correctness** over code coverage metrics:
- Simulation results must be mathematically sound (convergence curves match theory).
- Auth/RBAC must block unauthorized access.
- Data integrity: no NaN, Inf, or negative values in results.
- API contracts: endpoints return documented JSON structure.

## 16.1 Functional Validation

1. All major endpoints return expected HTTP status codes
2. Role-based controls return 401/403 where applicable
3. Dashboard updates across sections after simulation
4. Non-admin users blocked from sensitive endpoints

## 16.2 Data Integrity Validation

1. No NaN/Inf values in key metrics
2. Value range checks (fairness in [0,1], energy >= 0)
3. Convergence monotonically increases or stays flat
4. Deterministic constraints with fixed seeds where applicable

## 16.3 Deployment Validation

1. Local compile-check with `python -m py_compile`
2. Health endpoint returns 200 post deploy
3. Login flow works for all four accounts
4. Charts render after successful simulation

---

## 17. Operational Runbook

## 17.1 Start Locally

```bash
python app.py
```

## 17.2 Basic Smoke Test

1. open `/login`
2. login with a valid user
3. run transient simulation
4. verify chart updates

## 17.3 Admin Smoke Test

1. login as admin
2. run execute experiment
3. open experiments list and retrieval APIs
4. confirm session logs endpoint works

## 17.4 Common Failures

### A) Missing dependencies at deploy

Symptom:

- `ModuleNotFoundError` during gunicorn startup

Action:

1. add package to `requirements.txt`
2. redeploy with cache clear

### B) Python version incompatibility

Symptom:

- wheels/build failures on latest Python

Action:

1. pin runtime Python in `render.yaml` (`3.11.9`)
2. ensure scientific package versions match runtime

### C) Headless plotting backend issues

Symptom:

- matplotlib backend/display errors on server

Action:

- force `Agg` backend in plotting module

---

## 18. Extension Blueprint

## 18.1 Short-Term Enhancements

1. password reset and forced password change flow
2. login lockout/throttling
3. session timeout and idle logout
4. per-role UI menu metadata from backend API

## 18.2 Mid-Term Enhancements

1. persistent DB for experiments (PostgreSQL)
2. async task queue for long experiment runs
3. websocket stream updates for real-time progress
4. object storage for exported artifacts

## 18.3 Long-Term Enhancements

1. plugin-based strategy framework
2. scenario library and benchmark suites
3. multi-tenant workspace/project model
4. experiment lineage and provenance tracking
5. paper artifact packaging (dataset + config + outputs)

---

## 19. End-to-End User Journeys

## 19.1 Team Member Journey (mugdhi/sanya/evaluator)

1. Login
2. Configure nodes
3. Apply sample preset
4. Run transient simulation
5. Analyze charts and trends
6. Logout

Constraints:

- cannot access admin-sensitive experiment/log endpoints
- cannot perform destructive node management actions

## 19.2 Admin Journey

1. Login as admin
2. Configure or clear nodes
3. Run simulations and execute persistent experiments
4. Compare experiments
5. export data
6. review session logs
7. manage operational checks

---

## 20. Glossary

- FL: Federated Learning
- FedAvg: Federated Averaging aggregation algorithm
- SLA: Service-Level Agreement threshold/compliance
- RBAC: Role-Based Access Control
- Transient simulation: run without persistence
- Persistent experiment: saved run with metadata
- Green score: sustainability-oriented composite metric

---

## 21. Quick Reference Commands

## Local

```bash
python app.py
```

## Compile check

```bash
python -m py_compile app.py config.py
```

## Render deploy commands (conceptual)

- Build: install requirements
- Start: gunicorn app binding to `$PORT`

---

## 22. Final Notes

This project is already at a strong advanced state for:

- capstone demonstration,
- research experimentation,
- strategy comparison studies,
- interactive engineering showcase.

For public internet production use, the next major milestone is security hardening + persistent storage + operational monitoring.

---

## 23. Change Log Reference (High-Level)

1. dashboard upgrades and chart system expansion
2. realistic simulation engine integration
3. transient vs persistent API separation
4. role-based login gate and session logging
5. Render production deployment setup
6. dependency and headless plotting fixes for cloud runtime

---

## 24. Appendix: Suggested Figures for Reports/Papers

1. System Architecture Diagram
2. Proposed Methodology Flowchart
3. Experimental Setup Diagram
4. Strategy Comparison Dashboard Snapshot
5. Fairness vs Energy Tradeoff Plot
6. Carbon Impact Trend by Strategy
7. Communication Overhead Comparison

---

## 25. Appendix: Recommended Production Checklist

1. Replace all default passwords with strong unique values
2. Set strong random `FLASK_SECRET_KEY`
3. Ensure `FLASK_DEBUG=false`
4. Enable secure cookies and HTTPS-only policies
5. Restrict admin account usage and rotate credentials
6. Add rate limiting and login lockout
7. Move experiment storage from memory to DB
8. Add backup and retention policy for logs
9. Add alerting for repeated login failures
10. Add synthetic health probes for all critical endpoints

---

## 26. Consolidated Quickstart and Testing (Merged)

This section consolidates operational guidance that previously existed across multiple quickstart/testing markdown files.

## 26.1 First-Time Usage (5-10 Minutes)

1. Open the app and sign in at `/login`.
2. Go to Node Configuration and add nodes (or apply a preset).
3. Run a transient simulation (`Run Simulation`) for fast preview.
4. If you are admin, run persistent execution (`Execute Experiment`) to store and compare.
5. Review metrics and charts in Dashboard/Analytics/Strategies sections.

## 26.2 Recommended Initial Node Set

For meaningful visuals and comparisons, start with 4-10 nodes across mixed types:

1. edge/user devices for low-power behavior,
2. compute/data-center nodes for high-throughput behavior,
3. mixed regions (clean/mixed/fossil) for carbon analysis.

## 26.3 Key Metrics to Validate per Run

1. `avg_energy` and `total_energy`
2. `fairness_score` (0 to 1)
3. `convergence_metric` (0 to 1)
4. `communication_mb`
5. `carbon_footprint_kg`
6. `sla_violations`

## 26.4 Manual Testing Checklist

### Core flow

1. Add nodes.
2. Run simulation.
3. Confirm KPIs populate.
4. Confirm dashboard charts populate.
5. Confirm round table populates.

### Analytics flow

1. Visit Federated Analytics section.
2. Validate multi-line, heatmap, box, scatter, histogram, radar, ROC, and PR curves.
3. Validate no placeholder remains after successful run.

### RBAC flow

1. Login as team member (`mugdhi`, `sanya`, or `evaluator`):
  - verify admin controls are hidden,
  - verify admin-only API calls return `403`.
2. Login as `admin`:
  - verify full controls visible,
  - verify experiments/log APIs work.

### Export/log flow

1. As admin, test CSV/JSON export.
2. Verify `logs/user_sessions_log.csv` receives activity records.

## 26.5 API Usage Examples (Merged)

### Run transient simulation

```bash
curl -X POST http://localhost:5000/api/simulations/run \
  -H "Content-Type: application/json" \
  -d '{"strategy":"Federated Learning","rounds":5}'
```

### Execute persistent experiment (admin)

```bash
curl -X POST http://localhost:5000/api/experiments/execute \
  -H "Content-Type: application/json" \
  -d '{"name":"My Experiment","strategy":"Energy-Aware Heuristic","rounds":10}'
```

### List experiments (admin)

```bash
curl http://localhost:5000/api/experiments/list
```

### Get experiment detail (admin)

```bash
curl http://localhost:5000/api/experiments/1
```

### Delete experiment (admin)

```bash
curl -X DELETE http://localhost:5000/api/experiments/delete/1
```

## 26.6 Dashboard Chart UX Notes (Merged)

1. Chart modebar/tools are hover-visible by design.
2. Expand button is hover-visible and supports fullscreen chart inspection.
3. `Esc` closes expanded chart views.
4. Layout is responsive for desktop/tablet/mobile.
5. Plotly export as PNG is available from chart modebar.

## 26.7 Common User-Side Issues and Fixes

1. Empty charts after loading app:
  - run at least one simulation,
  - verify nodes are configured.
2. `No nodes configured` error:
  - add nodes or apply sample preset first.
3. Strategy/API 400 errors:
  - ensure valid strategy names and numeric ranges.
4. Permission errors (403):
  - expected for non-admin users on sensitive endpoints.

## 27. Consolidation Note

This `PROJECT.md` is now the canonical master documentation source for the repository.
Redundant legacy quickstart/summary/guide markdown files have been removed from the main documentation set.

---

### End of Master Document
