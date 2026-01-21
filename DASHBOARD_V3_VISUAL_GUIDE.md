# DASHBOARD v3.0 - Visual Reference Guide

## 🎨 Dashboard Layout Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                          HEADER                                   │
│  Dashboard Overview          [Run Simulation] [Export]            │
├─────────────┬────────────────────────────────────────────────────┤
│  SIDEBAR    │                   MAIN CONTENT AREA                │
│             │                                                      │
│  Dashboard  │  ┌─ KPI ROW ──────────────────────────────────────┐│
│  🏠         │  │ Energy  SLA  Fairness  Carbon  Nodes  Strategy ││
│             │  └──────────────────────────────────────────────────┘│
│  Nodes      │                                                      │
│  🖥️         │  ┌─ CHARTS (2x2 Grid) ───────────────────────────┐ │
│             │  │ Loss Chart    │ Resource Util                  │ │
│  Strategies │  ├────────────────┼──────────────────────────────┤ │
│  ⚖️        │  │ Metrics Pie   │ Client Performance             │ │
│             │  └────────────────┴──────────────────────────────┘ │
│  Analytics  │                                                      │
│  📊         │  ┌─ TABLE ─────────────────────────────────────────┐ │
│             │  │ Round | Loss | CPU | Memory | Duration | Status │ │
│  Fairness   │  └────────────────────────────────────────────────┘ │
│  🍃         │                                                      │
│             │                                                      │
│  Experiments│                                                      │
│  🔬         │                                                      │
│             │                                                      │
│  Logs       │                                                      │
│  📁         │                                                      │
│             │                                                      │
│  About      │                                                      │
│  ❓         │                                                      │
└─────────────┴────────────────────────────────────────────────────┘
```

## 🎯 KPI Cards

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│    ⚡    │  │   ⚠️    │  │    ⚖️    │  │   🍃    │  │   🖥️    │  │    ⚙️    │
│  Energy  │  │   SLA    │  │ Fairness │  │  Carbon  │  │  Nodes   │  │ Strategy │
│          │  │          │  │          │  │          │  │          │  │          │
│ XX.XX    │  │   X      │  │ 0.XXX    │  │ XX.XX    │  │    X     │  │ Federated│
│  kWh     │  │  Count   │  │  Score   │  │ kg CO₂   │  │  Count   │  │ Learning │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘

Each card has:
• Color-coded icon
• Gradient top border (cyan → green)
• Hover effect (lift + shadow + glow)
• Real-time value updates
```

## 📊 Visualization Suite Map

```
DASHBOARD OVERVIEW
├── Line Chart (Loss Progression)
│   └── Traces: Avg Loss over rounds with area fill
│
├── Stacked Area (Resources)
│   └── Traces: CPU%, Memory%, Disk% stacked over time
│
├── Pie/Donut (Metrics Distribution)
│   └── Slices: Energy, SLA, Fairness, Rounds
│
└── Grouped Bar (Client Performance)
    └── Bars: Loss per client (last round)

FEDERATED ANALYTICS
├── Multi-Line (Loss vs Resources)
│   └── Traces: Loss (left axis) + CPU/Memory (right axis)
│
├── Heatmap (Client-Round Matrix)
│   └── Cells: Client losses by round (color intensity)
│
├── Box Plot (Distribution by Round)
│   └── Boxes: Loss distribution for each round
│
├── Scatter Plot (CPU vs Loss)
│   └── Points: Rounds colored by sequence
│
├── Histogram (Loss Frequency)
│   └── Bins: Frequency distribution of all losses
│
└── Radar Chart (Multi-Metric Profile)
    └── Axes: Fairness, SLA Compliance, Energy, Sustainability
```

## 🎨 Color System

```
PRIMARY COLORS:
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   #0f172a   │ │   #38bdf8   │ │   #22c55e   │ │   #ef4444   │
│  Background │ │   Primary   │ │   Success   │ │    Error    │
│ Dark Slate  │ │    Cyan     │ │    Green    │ │     Red     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

SECONDARY COLORS:
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   #111827   │ │   #1f2933   │ │   #f59e0b   │ │   #9ca3af   │
│  Card Dark  │ │ Card Light  │ │   Warning   │ │ Text Subtle │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

USAGE PATTERNS:
• Backgrounds: #0f172a (main), #111827 (cards)
• Text: #e5e7eb (primary), #9ca3af (secondary)
• Accents: #38bdf8 (interactive elements)
• Status: Green (success), Red (error), Amber (warning)
```

## 🧭 Sidebar Navigation Map

```
SIDEBAR
├── 📊 Dashboard Overview
│   └── → Landing page with KPIs & summary
│
├── 🖥️ Node Configuration
│   └── → Add/edit/delete nodes, run custom simulation
│
├── ⚖️ Strategy Comparison
│   └── → Compare 4 strategies across metrics
│
├── 📈 Federated Analytics
│   └── → 6 chart types, advanced analysis
│
├── 🍃 Fairness & Sustainability
│   └── → Fairness heatmaps, carbon footprint
│
├── 🔬 Experiments
│   └── → Experiment history, comparison
│
├── 📁 Logs & Export
│   └── → Export CSV/JSON/PDF, view raw data
│
└── ❓ About / Help
    └── → Documentation, shortcuts, resources
```

## 📱 Responsive Breakpoints

```
DESKTOP (>1200px)
┌─────────┬──────────────────────┐
│         │                      │
│ Sidebar │ 2-3 Column Grid      │
│ 260px   │ Full Width Content   │
│         │                      │
└─────────┴──────────────────────┘

TABLET (768-1200px)
┌─────────┬──────────────────────┐
│         │                      │
│ Compact │ 1-2 Column Grid      │
│ Sidebar │ Responsive Content   │
│ 70px    │                      │
└─────────┴──────────────────────┘

MOBILE (<768px)
┌──────────────────────────────┐
│  [≡] Header                  │
├──────────────────────────────┤
│  Hamburger Sidebar           │
│  Full Width Content          │
│  Single Column               │
└──────────────────────────────┘
```

## ⚙️ Interactive Features Map

```
CHARTS
Every chart includes:
├── Hover Tooltip
│   └── Shows: Values, labels, additional data
├── Legend Toggle
│   └── Click legend items to show/hide
├── Zoom & Pan
│   └── Drag to zoom, double-click to reset
├── Export Button
│   └── Download as PNG image
└── Responsive
    └── Auto-resize with viewport

FORMS
├── Node Creation Form
│   ├── Type dropdown (4 options)
│   ├── CPU cores number input
│   ├── Memory (GB) number input
│   ├── Energy cost factor
│   ├── SLA threshold %
│   ├── Region selector
│   └── Add/Clear buttons
│
└── Simulation Control
    ├── Strategy selector
    ├── Rounds input
    ├── Parameter sliders
    └── Execute button

TABLES
├── Sortable columns (click headers)
├── Hover highlighting
├── Row actions (delete, edit)
├── Status badges
└── Search/filter (future)
```

## 🎨 Card Design Anatomy

```
CARD STRUCTURE
┌─────────────────────────────────────┐
│ Title with Icon                     │
├─────────────────────────────────────┤
│                                     │
│  Content Area (Chart, Form, Table)  │
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘

STYLING:
• Bg: #111827 (dark)
• Border: 1px solid #1f2937
• Corner: 8px border-radius
• Shadow: 0 4px 6px rgba(0,0,0,0.3)
• Hover: Border color → #38bdf8, shadow enhanced

TITLE:
• Icon: 1.5rem, #38bdf8
• Text: 1.3rem, bold, #e5e7eb
• Layout: flex, gap 10px
```

## 📋 Form Element Styles

```
INPUTS
┌─────────────────────────────────┐  Text: #e5e7eb
│ Label (above)                   │  Bg: #1f2933
├─────────────────────────────────┤  Border: 1px #1f2937
│                                 │  Focus: Cyan glow
│ Input field                     │  Corner: 6px
│                                 │  Padding: 10px 12px
└─────────────────────────────────┘

SELECTS
Same styling as inputs
With dropdown arrow

BUTTONS
Primary:  Bg #38bdf8, Text dark
Success:  Bg #22c55e, Text dark
Danger:   Bg #ef4444, Text white
Warning:  Bg #f59e0b, Text dark

Hover: Translate up -2px, shadow enhanced
```

## 🔤 Typography Scale

```
Header Title:    1.8rem, 700 weight, #e5e7eb
Card Title:      1.3rem, 700 weight, #e5e7eb
Form Label:      0.9rem, 600 weight, #e5e7eb
Table Header:    0.8rem, 700 weight, #38bdf8 (uppercase)
Body Text:       0.95rem, 400 weight, #e5e7eb
Secondary:       0.9rem, 400 weight, #9ca3af
Small:           0.85rem, 400 weight, #9ca3af
```

## 🎬 Animation Definitions

```
TRANSITIONS (0.3s ease)
• Sidebar collapse/expand
• Chart redraw
• Hover effects
• Color changes
• Border transitions

KEYFRAME ANIMATIONS
@fadeIn (0.3s)
  from: opacity 0, translateY 10px
  to:   opacity 1, translateY 0

@spin (1s infinite)
  0%:   transform rotate(0deg)
  100%: transform rotate(360deg)

Applied to:
• Section switches (fadeIn)
• Loading spinners (spin)
• Button interactions (transitions)
```

## 📊 Data Flow Visualization

```
USER INTERFACE (dashboard_v3.html)
        ↓ [Click / Input]
JAVASCRIPT (Event Handlers)
        ↓ [Validation]
API CALLS (fetch /api/*)
        ↓ [Network Request]
FLASK BACKEND (app.py routes)
        ↓ [Processing]
PYTHON SERVICES (orchestration, metrics)
        ↓ [JSON Response]
PLOTLY.JS (Chart Rendering)
        ↓ [DOM Manipulation]
BROWSER DISPLAY (Interactive Charts)
```

## 🎯 Section Purposes Quick Reference

| Section | Purpose | Key Features |
|---------|---------|--------------|
| Dashboard | Overview & KPIs | 6 KPI cards, 4 charts, summary table |
| Nodes | Configuration | Add/delete nodes, custom simulation |
| Strategies | Comparison | Filter metrics, 2 chart types |
| Analytics | Deep Dive | 6 advanced charts, round slider |
| Fairness | Sustainability | 4 visualizations, node breakdown |
| Experiments | History | Results table, comparison charts |
| Logs | Export & Debug | CSV/JSON export, raw data viewer |
| About | Documentation | Help, shortcuts, resources |

---

## 🚀 Quick Start for Users

1. **Arrive at Dashboard** → See KPIs and summary
2. **Go to Node Config** → Add cloud nodes
3. **Run Simulation** → Execute with parameters
4. **View Results** → All charts auto-populate
5. **Explore Metrics** → Switch to Analytics for deep dive
6. **Export Data** → Download results (CSV/JSON)

---

## ⚡ Performance Characteristics

- **Page Load Time**: <2 seconds
- **Chart Render Time**: <1 second (Plotly.js)
- **Sidebar Toggle**: 0.3 seconds (smooth)
- **Section Switch**: Instant (pre-loaded)
- **Export Time**: <1 second (CSV)
- **Memory Usage**: ~50-100 MB (browser)
- **Network**: Single large request for Plotly.js library

---

**This visual reference guide complements the full DASHBOARD_V3_UPGRADE.md documentation.**
