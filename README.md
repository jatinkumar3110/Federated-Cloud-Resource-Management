# 🌐 Federated Learning–Driven Resource Management for Cloud Computing Environments

> A research-grade platform for privacy-preserving, sustainability-aware resource optimization in heterogeneous cloud environments using federated learning.

---

## 📚 Documentation Map

Find what you need quickly:

| Document | Purpose | Audience |
|----------|---------|----------|
| **README.md** (you are here) | Quick overview, features, setup, API reference | Everyone - GitHub landing page |
| **[PROJECT.md](PROJECT.md)** | 📖 Master technical document (27 sections, 3000+ lines) | Developers, researchers, operators |
| **[summary.txt](summary.txt)** | 💼 Concise project status and capabilities | Project managers, quick reference |

### What to Read When:

- **Just heard about this? Start here** → README.md (this file)
- **Need to understand architecture?** → PROJECT.md Section 5-7
- **Deploying to production?** → PROJECT.md Section 13 + Section 25 (security checklist)
- **Implementing new features?** → PROJECT.md Section 7 (module guide)
- **Researching federated learning?** → PROJECT.md Section 3.5 (FL primer) + Section 18 (examples)
- **Security concerns?** → PROJECT.md Section 14 (threat modeling, hardening roadmap)
- **Quick status check?** → summary.txt

---

## ✨ Project Overview

A **research-grade** capstone project implementing **federated learning** for privacy-preserving, energy-efficient resource management across heterogeneous cloud nodes.

### 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🔐 **Privacy-First** | Federated averaging (FedAvg) algorithm—no raw data centralization |
| ⚡ **Multi-Objective** | Simultaneously optimize energy, cost, SLA, fairness, sustainability |
| 📊 **Realistic Simulation** | Physics-based energy models, carbon footprint by region, convergence curves |
| 🎨 **Interactive Dashboard** | Professional console-style UI with real-time charts, advanced analytics |
| 🔄 **Dual Execution Modes** | Transient simulations (instant exploration) + persistent experiments (reproducible research) |
| 🛡️ **Security Built-In** | Role-based login (admin + team users), session audit logging, password hashing |
| ☁️ **Cloud-Ready** | Render-ready production deployment, gunicorn + Python 3.11.9, environment-driven config |
| 📈 **Research-Grade** | Reproducible metric generation, paper-ready visualizations, experiment tracking |

---

## 🏗️ Architecture Overview

### Layered Design (Strict Separation of Concerns)

```
┌─────────────────────────────────────────────────────────────────┐
│  🎨 PRESENTATION LAYER (Web UI)                                 │
│  ├─ templates/dashboard_v3.html: Interactive research console   │
│  └─ templates/login.html: Authentication gate                   │
├─────────────────────────────────────────────────────────────────┤
│  🔌 API / WEB LAYER (app.py)                                    │
│  ├─ Flask HTTP routing, authentication, RBAC enforcement        │
│  └─ JSON serialization, error handling, session management      │
├─────────────────────────────────────────────────────────────────┤
│  🎯 ORCHESTRATION LAYER (app coordination)                      │
│  ├─ orchestration.py: Workflow & simulation coordination        │
│  ├─ orchestration_nodes.py: Node lifecycle management           │
│  └─ experiments/: Scenario definition, experiment execution     │
├─────────────────────────────────────────────────────────────────┤
│  🔬 SIMULATION & SCIENCE LAYER (Core Logic)                     │
│  ├─ simulation_data_generator.py: Physics-based metrics         │
│  ├─ simulation/*.py: Node simulation, workload models           │
│  ├─ metrics/*.py: Fairness, energy, carbon, communication       │
│  ├─ federated/*.py: FedAvg aggregation algorithms               │
│  └─ visualization/*.py: Chart rendering and export              │
└─────────────────────────────────────────────────────────────────┘
```

**Design Philosophy**: Each layer only knows about the layer directly below it. This enforces modularity, testability, and allows independent evolution.

### Execution Flow

```
User Input (Dashboard)
    ↓
[1] Configure nodes (manual or apply presets)
    ↓
[2] Select strategy & parameters (rounds, weights)
    ↓
[3] Choose execution mode:
    → Transient: Run & discard (instant exploration)
    → Persistent: Save for comparison (reproducible research)
    ↓
[4] Orchestration: Initialize nodes + strategy
    ↓
[5] Simulation Engine: Generate round-by-round metrics
    ├─ Energy model (per-node, per-round)
    ├─ Communication overhead (uplink + downlink)
    ├─ Convergence progression (exponential model)
    ├─ Fairness variance (heterogeneity impact)
    └─ Carbon footprint (region-weighted)
    ↓
[6] Metrics Aggregation: Compute final KPIs
    ↓
[7] Visualization: Render dashboard charts (Plotly)
    ↓
Result: Metrics, charts, logs + optional CSV export (admin)
```

---

## 📁 Repository Structure

```
federated_cloud_dashboard/
│
├── Core Application Entry Point
│   ├── app.py                           # 🔌 Flask WSGI app, HTTP routes, auth, RBAC, APIs
│   ├── config.py                        # ⚙️ Environment-driven configuration
│   └── requirements.txt                 # 📦 Python dependencies
│
├── Deployment Configuration
│   ├── render.yaml                      # ☁️ Render cloud deployment (Python 3.11.9, gunicorn)
│   ├── Procfile                         # 🚀 WSGI startup command
│   ├── PROJECT.md                       # 📖 Master technical documentation (27 sections)
│   └── summary.txt                      # 📄 Project status summary
│
├── Orchestration & Workflow
│   ├── orchestration.py                 # 🎯 Pipeline & simulation coordinator
│   ├── orchestration_nodes.py           # 🖥️ Node configuration manager (CRUD)
│   │
│   └── experiments/                     # 🧪 Reproducible experiment management
│       ├── scenario_manager.py          # Scenario definition & templating
│       └── experiment_runner.py         # Execution orchestration & aggregation
│
├── Federated Learning (Core Science)
│   └── federated/                       # 🤖 FL algorithms
│       ├── model.py                     # Model architecture
│       └── trainer.py                   # FedAvg aggregation, client/server logic
│
├── Simulation Engine (Metric Generation)
│   ├── simulation_data_generator.py     # 🔬 Realistic metrics: energy, carbon, fairness, convergence
│   │
│   └── simulation/                      # 📡 Node-level simulation
│       ├── node.py                      # Node abstraction
│       ├── node_types.py                # Edge, compute, storage types
│       ├── workload.py                  # Synthetic workload generation
│       └── resource_monitor.py          # CPU/memory/disk monitoring
│
├── Metrics & Evaluation (Research Analysis)
│   └── metrics/                         # 📊 Domain-specific metrics
│       ├── evaluator.py                 # Performance summaries & scoring
│       ├── fairness.py                  # Heterogeneity impact analysis
│       ├── communication.py             # Bandwidth utilization metrics
│       └── sustainability.py            # Energy & carbon impact
│
├── Visualization & Plotting
│   └── visualization/                   # 📈 Chart generation
│       ├── plot_generator.py            # Matplotlib helpers (Agg backend for cloud)
│       └── comparison_plots.py          # Multi-strategy visualizations
│
├── User Interface (Web Frontend)
│   └── templates/                       # 🎨 Jinja2 HTML templates
│       ├── dashboard_v3.html            # Main professional research console
│       ├── dashboard.html               # Legacy dashboard (v2)
│       └── login.html                   # Authentication gate
│
├── Static Assets
│   └── static/                          # 🎨 CSS, JavaScript, images
│       └── style.css                    # Dashboard styling
│
├── Audit & Logging
│   └── logs/                            # 📋 Runtime logs & activity
│       ├── metrics_log.csv              # Simulation metrics history
│       └── user_sessions_log.csv        # Login, API calls, access denials (audit trail)
│
├── Public Distribution
│   └── public_repo/                     # 📦 GitHub-ready version (README, simplified docs)
│
└── Testing & Validation
    ├── test_pipeline.py                 # Integration test suite
    └── generate_documentation_images.py # Diagram generation
```

**Color Legend**: 🔌 Web | ⚙️ Config | 📦 Dependencies | ☁️ Deployment | 🎯 Orchestration | 🖥️ Nodes | 🧪 Experiments | 🤖 ML | 🔬 Science | 📡 Simulation | 📊 Metrics | 📈 Charts | 🎨 UI | 📋 Logs

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.11+ (3.11.9 recommended for cloud compatibility)
- pip (comes with Python)
- Virtual environment support
- ~100 MB disk space + ~200 MB for dependencies

### Local Development Setup

```bash
# 1. Clone repository
git clone <your-repo-url>
cd Federated_Cloud_Dashboard

# 2. Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

✅ **Success**: App is live at `http://127.0.0.1:5000`

### First-Time Usage

1. **Login**: Use account `admin` / `dev_default_change_me` (default credentials)
2. **Add Nodes**: Click "Node Configuration" → "Sample 5 Nodes" preset
3. **Run Simulation**: Click "Run Simulation" → observe dashboard charts populate
4. **Explore**: Switch tabs to view analytics, fairness metrics, energy breakdown

**Note**: Credentials change to environment variables in production (see [PROJECT.md](PROJECT.md) Section 13)

---

## 🔧 Key Components & Their Roles

| Component | File | Responsibility |
|-----------|------|-----------------|
| **Flask Application** | `app.py` | HTTP routing, authentication (login/logout), role-based access control (RBAC), API endpoints, session management, user activity logging |
| **Configuration** | `config.py` | Environment-driven runtime settings (DEBUG, HOST, PORT, auth), federated defaults, simulation bounds, metric norms |
| **Orchestration** | `orchestration.py` | Workflow coordinator: validates inputs, initializes nodes + strategy, calls simulation engine, aggregates results |
| **Node Manager** | `orchestration_nodes.py` | Node lifecycle (CRUD), validation, presets (sample cluster, heterogeneous fleet) |
| **Simulation Engine** | `simulation_data_generator.py` | **Core research logic**: Physics-based energy model, communication overhead, convergence progression, fairness variance, carbon footprint (region-weighted) |
| **Experiments** | `experiments/*` | Scenario templating, persistent execution, result aggregation (for reproducible research workflows) |
| **Federated Learning** | `federated/trainer.py` | FL-specific: Client update generation, server aggregation (FedAvg, weighted, energy-aware variants) |
| **Metrics** | `metrics/*` | Research metrics: fairness (variance-based), communication (MB totals), sustainability (energy + carbon), convergence summaries |
| **Visualization** | `visualization/*` | Plotly chart rendering (all metrics), comparison plots, export to PNG/PDF (paper use) |
| **Dashboard UI** | `templates/dashboard_v3.html` | Interactive research console: 8 sections (Overview, Nodes, Strategies, Analytics, Fairness, Experiments, Compare, Logs) + role-based control hiding |
| **Authentication UI** | `templates/login.html` | Session login gate with error feedback, account hint |
| **Logging** | `logs/` | Audit trail (user_sessions_log.csv: login, API calls, denials) + optional metrics history |

---

## 🔌 API Endpoints Reference

### Authentication & Session (🔐 Auth Gate)

| Method | Endpoint | Purpose | Access | Returns |
|--------|----------|---------|--------|---------|
| GET | `/login` | Display login form | Public | HTML page |
| POST | `/login` | Process login credentials | Public | 302 redirect or error |
| GET\|POST | `/logout` | Clear session & logout | Authenticated | Redirect to `/login` |
| GET | `/api/auth/me` | Get current user + role | Authenticated | {username, role} |

### Core Simulation (🧬 Research)

| Method | Endpoint | Purpose | Access | Returns |
|--------|----------|---------|--------|---------|
| POST | `/api/simulations/run` | Run transient simulation | Authenticated | Final metrics + round results |
| POST | `/api/experiments/execute` | Execute persistent experiment | Admin | Saved experiment ID + metrics |
| GET | `/api/experiments/list` | List all saved experiments | Admin | Array of experiments |
| GET | `/api/experiments/<id>` | Retrieve single experiment | Admin | Experiment detail |
| DELETE | `/api/experiments/delete/<id>` | Delete experiment | Admin | Success confirmation |

### Node Management (🖥️ Cluster Config)

| Method | Endpoint | Purpose | Access | Returns |
|--------|----------|---------|--------|---------|
| GET | `/api/nodes` | List configured nodes | Authenticated | Array of node definitions |
| POST | `/api/nodes` | Add new node | Authenticated | New node ID + config |
| PUT | `/api/nodes/<node_id>` | Modify node properties | Admin | Updated node |
| DELETE | `/api/nodes/<node_id>` | Delete node | Admin | Success confirmation |
| POST | `/api/nodes/clear` | Clear all nodes | Admin | Success confirmation |

### Metrics & Analytics (📊 Results)

| Method | Endpoint | Purpose | Access | Returns |
|--------|----------|---------|--------|---------|
| GET | `/api/metrics/current` | Latest simulation metrics | Authenticated | Energy, fairness, carbon, convergence |
| GET | `/api/model/state` | Internal model state dump | Admin | Full state object |
| POST | `/api/metrics/fairness` | Compute fairness metrics | Authenticated | Fairness details |
| POST | `/api/metrics/communication` | Compute communication | Authenticated | Communication breakdown |
| POST | `/api/metrics/sustainability` | Compute carbon & energy | Authenticated | Energy + carbon impact |

### Health & Operations (⚙️ Deployment)

| Method | Endpoint | Purpose | Access | Returns |
|--------|----------|---------|--------|---------|
| GET | `/api/health` | Service health check | Public | {status: healthy, timestamp, version} |
| GET | `/api/session-logs` | User activity audit log | Admin | CSV-formatted audit trail |
| GET | `/` | Dashboard home page | Authenticated | HTML dashboard |

---

## ⚙️ Configuration & Environment Variables

### Local Development (Defaults in config.py)

- DEBUG = True (hot reload)
- FLASK_SECRET_KEY = dev_insecure_... (for local testing)
- HOST = localhost (local only)
- PORT = 5000 (Flask default)

### Production (Render Cloud)

Set via Render dashboard → Environment variables:

```
FLASK_SECRET_KEY=64-char-hex-from-openssl-rand-hex-32
FLASK_DEBUG=false
ADMIN_PASSWORD=strong-random-string
MUGDHI_PASSWORD=strong-random-string
SANYA_PASSWORD=strong-random-string
EVALUATOR_PASSWORD=strong-random-string
```

For full configuration guide, see [PROJECT.md](PROJECT.md) Section 13 (Deployment Architecture)

---

## Testing

Run baseline validation:

```bash
python test_pipeline.py
python -m py_compile app.py config.py
```

Manual validation:

1. Login with a valid account.
2. Add nodes or apply sample preset.
3. Run simulation and verify charts update.
4. Confirm admin-only controls are hidden for team users.
5. As admin, confirm experiment APIs and session log API work.

---

## 🎯 Research Contributions

This platform enables critical research in multiple dimensions:

| Research Area | Contribution |
|---------------|--------------|
| **Privacy & Security** | Federated averaging avoids data centralization |
| **Energy Efficiency** | Physics-based models; carbon footprint by region |
| **Fairness in ML** | Heterogeneous node convergence analysis |
| **Communication Efficiency** | Network overhead modeling; bottleneck analysis |
| **Sustainability** | Multi-objective optimization; CO2 impact |
| **Strategy Comparison** | Static vs Centralized vs Federated vs Energy-Aware |

---

## 🏛️ Architectural Principles (Strict Rules)

✅ Single Responsibility: Each module owns one domain  
✅ Layered Design: Clean UI → Web → Orchestration → Science boundaries  
✅ Flask as Gateway: HTTP layer doesn't implement core logic  
✅ Environment-Driven: All secrets and config from environment variables  
✅ Role-Based Security: Sensitive operations protected via RBAC middleware  
✅ Audit Logging: All API calls and denials logged to CSV  
✅ Cloud-Ready: Headless matplotlib, gunicorn compatible, Render-optimized

---

## 📋 Debugging & Operations Guide

### Main Log Files

- `logs/user_sessions_log.csv`: Login, logout, API calls, access denials (audit trail)
- `logs/metrics_log.csv`: Optional simulation metrics history
- Terminal output: Flask logs, error stack traces, DEBUG details

### Standard Checks

1. **Service Health**: `curl http://localhost:5000/api/health`
2. **Render Deployment Issues**: Check render logs in Render dashboard → Logs tab
3. **User Activity**: Review `logs/user_sessions_log.csv` for access patterns and denials

### Troubleshooting Common Problems

| Issue | Symptom | Solution |
|-------|---------|----------|
| **Missing Package** | ModuleNotFoundError at startup | Add to requirements.txt, run `pip install -r requirements.txt` |
| **Python Version** | Wheel build fails | Use Python 3.11.9 (pinned for Render) |
| **Plotting Errors** | Display backend errors on server | Verify `matplotlib.use('Agg')` in visualization/plot_generator.py |
| **Port Conflict** | Address already in use | Try `PORT=5001 python app.py` |
| **Blank Dashboard** | No charts appear | Run at least one simulation first |
| **Auth 401** | Login fails on all endpoints | Check session cookie, verify login succeeded |
| **Admin Denied (403)** | Can't access /api/experiments/list | Must login as admin account |

### Quick Health Check

```
HTTP GET /api/health
Expected Response: 200 OK
{status: healthy, timestamp: 2025-03-17T..., version: 1.0.0}
```

---

## ❓ FAQ

**Q: Separate frontend hosting needed?**  
A: No. Flask serves everything. Single unified deployment.

**Q: Can non-admins run simulations?**  
A: Yes. All users can run transient sims. Persistent experiments are admin-only.

**Q: Why experiments admin-only?**  
A: Prevent accidental deletion of research runs.

**Q: How to deploy publicly?**  
A: Commit to GitHub → Connect Render → Set secrets → Deploy (1-click, 2-3 min).

**Q: Data persistent after restart?**  
A: In-memory; lost on restart. Use PostgreSQL for production.

**Q: Run on my laptop?**  
A: Yes! Just `python app.py`. Perfect for development.

**Q: Modify the dashboard?**  
A: Edit `templates/dashboard_v3.html` + `static/style.css` + call APIs from JavaScript.

**Q: Implement new strategy?**  
A: Add to `config.py` → implement in `simulation_data_generator.py` →add UI button. See PROJECT.md Section 18.

---

## 🚀 Getting Started Now

### Option 1: Local (< 5 minutes)

```bash
python app.py
# http://localhost:5000
# Login: admin / dev_default_change_me
```

### Option 2: Cloud (5-10 minutes)

1. `git push` to GitHub
2. Connect Render to your repo
3. Set environment variables (FLASK_SECRET_KEY, passwords)
4. Deploy button

Full guide: [PROJECT.md](PROJECT.md) Section 13

---

## 📚 Full Documentation

| Need | Resource |
|------|----------|
| Architecture & modules | [PROJECT.md](PROJECT.md) Sections 5-7 |
| All APIs explained | [PROJECT.md](PROJECT.md) Section 10 |
| Deployment guide | [PROJECT.md](PROJECT.md) Section 13 |
| Security & hardening | [PROJECT.md](PROJECT.md) Sections 14-25 |
| Authentication details | [PROJECT.md](PROJECT.md) Section 9 |
| Testing & validation | [PROJECT.md](PROJECT.md) Section 16 |
| Operations runbook | [PROJECT.md](PROJECT.md) Section 17 |
| Extension roadmap | [PROJECT.md](PROJECT.md) Section 18 |
| FL primer | [PROJECT.md](PROJECT.md) Section 3.5 |
| Curl examples | [PROJECT.md](PROJECT.md) Section 26 |
| Production checklist | [PROJECT.md](PROJECT.md) Section 25 |
| Quick status | [summary.txt](summary.txt) |

---

## 📄 License

**Research Project** — Educational Use Only

---

**Version**: 1.0 | **Updated**: March 17, 2026 | **Status**: Production-Ready ✅
