# 🔄 Simulation Save & Compare Feature Guide

**New Feature**: Save multiple simulations and compare them side-by-side!

---

## ✨ What's New

✅ **Save Simulations** - Each simulation is auto-saved as "Simulation 1", "Simulation 2", etc.  
✅ **Compare Results** - View side-by-side comparison of energy, fairness, and other metrics  
✅ **Persistent Storage** - Simulations saved to browser storage (survives page refresh)  
✅ **New Section** - "Compare Sims" navigation item in sidebar  
✅ **Fixed Empty Sections** - All charts and tables now populate correctly  

---

## 🎯 How to Use

### **Step 1: Run Your First Simulation**

1. Go to **"🖥️ Node Configuration"**
2. Make sure you have 3-4 nodes configured
3. Click **"Execute Simulation"** button
4. Wait for completion (shows "✓ Simulation completed")

**Result**: 
- Simulation #1 saved automatically
- Dashboard updates with data
- All charts populate

### **Step 2: Run More Simulations**

Run another simulation with different parameters:

1. Go to **"🖥️ Node Configuration"** 
2. Scroll to "Run Custom Simulation" section
3. Change strategy or rounds (optional)
4. Click **"Execute Simulation"** again

**Result**: 
- Simulation #2 saved automatically
- New data displayed in dashboard
- Comparison section now active

### **Step 3: Compare Simulations**

Click **"📊 Compare Sims"** in sidebar

**You'll see**:
- ✅ **Saved Simulations List** - All your saved simulations (left panel)
- ✅ **Energy Consumption Comparison** - Bar chart comparing energy across sims
- ✅ **Fairness Score Comparison** - Bar chart comparing fairness scores
- ✅ **Comparison Results Table** - All metrics side-by-side

---

## 📊 Comparison Section Details

### **Saved Simulations List**
Shows all saved simulations with:
- Simulation name (Simulation 1, 2, 3, etc.)
- Timestamp (when it was run)
- Click to load any previous simulation
- View its results instantly

### **Energy Consumption Comparison**
- Bar chart showing energy used in each simulation
- Compare efficiency across different strategies
- Lower bars = more efficient

### **Fairness Score Comparison**
- Bar chart showing fairness in each simulation
- Compare fairness across different configurations
- Higher bars = more fair

### **Comparison Results Table**
Columns:
- **Simulation** - Name (Simulation 1, 2, 3)
- **Energy (kWh)** - Energy consumed
- **Fairness** - Fairness score (0-1)
- **SLA Violations** - Count of violations
- **Nodes** - Number of nodes used
- **Rounds** - Number of training rounds
- **Timestamp** - When simulation ran
- **Actions** - ↻ Reload or 🗑️ Delete

**Actions**:
- Click ↻ to reload that simulation and view its dashboard
- Click 🗑️ to delete that simulation

---

## 🔧 Fixed Issues

### **Issue 1: KPI Cards Showing 0.00**
✅ **FIXED** - Now correctly updates all KPI values:
- Total Energy
- SLA Violations
- Fairness Score
- Carbon Footprint
- Active Nodes
- Best Strategy

### **Issue 2: Strategy Section Empty**
✅ **FIXED** - Now populates when simulation runs:
- Grouped Comparison bar chart
- Radar chart
- Detailed Metrics table

### **Issue 3: Fairness Section Empty**
✅ **FIXED** - Now shows 4 charts:
- Node Fairness Heatmap
- Carbon Footprint Timeline
- Energy Source Mix pie chart
- Fairness vs Energy scatter

### **Issue 4: Experiments Section Empty**
✅ **FIXED** - Now records experiments:
- Experiment Results table (auto-logged)
- Energy Comparison chart
- Fairness Comparison chart

### **Issue 5: Logs Section Empty**
✅ **FIXED** - Now displays:
- Simulation Log (with timestamps)
- Raw Simulation Data (full JSON)

---

## 📈 Complete Workflow

```
1. Add Nodes
   ↓
2. Run Simulation #1
   ↓
   → Auto-saved as "Simulation 1"
   → All sections populate with data
   ↓
3. Go to Compare Sims section
   ↓
   → See energy comparison
   → See fairness comparison
   ↓
4. Run Simulation #2 (different settings)
   ↓
   → Auto-saved as "Simulation 2"
   ↓
5. Return to Compare Sims
   ↓
   → Now shows 2 bars on comparison charts
   → Table compares both simulations
   ↓
6. Click "Simulation 1" in left panel
   ↓
   → Dashboard reloads with Sim #1 data
   → Can view details
   ↓
7. Export data
   ↓
   → CSV with all simulation results
   → JSON with full raw data
```

---

## 🎯 Example: Testing the Feature

### **Test Scenario**

**Simulation 1**:
- 4 nodes (mixed types)
- 10 rounds
- Strategy: Federated Learning
- Optimization: Energy Efficiency

**Expected Results**:
```
Energy: ~240 kWh
Fairness: ~0.82
SLA Violations: 0-2
```

**Simulation 2**:
- Same 4 nodes
- 10 rounds  
- Strategy: Centralized
- Optimization: Fairness Focus

**Expected Results**:
```
Energy: ~320 kWh (higher)
Fairness: ~0.92 (higher)
SLA Violations: 0-1
```

**Comparison**:
- Energy bar chart shows Sim 1 < Sim 2
- Fairness bar chart shows Sim 1 < Sim 2
- Table shows all detailed metrics side-by-side

---

## 💾 Data Persistence

**Simulations are saved locally** in your browser:
- Survives page refresh (F5)
- Survives closing and reopening dashboard
- Stored in browser LocalStorage
- **Not deleted** unless you click 🗑️ button

**To clear all simulations**:
1. Open browser DevTools (F12)
2. Go to Application tab
3. Find LocalStorage
4. Delete `savedSimulations` entry
5. Refresh page

---

## 🐛 Troubleshooting

### **Charts Not Showing Data**
1. Make sure you ran at least 1 simulation
2. Check browser console (F12 → Console) for errors
3. Refresh page (F5)
4. Run simulation again

### **Comparison Section Empty**
You need at least 2 simulations:
1. Run first simulation
2. Run second simulation
3. Go to "Compare Sims" section
4. Charts should appear with 2 bars each

### **KPI Values Still 0.00**
1. Check that simulation completed (look for "✓ Simulation completed")
2. Check browser console for JS errors
3. Try running simulation again
4. Refresh page if still empty

### **Simulations Not Saving**
1. Browser LocalStorage might be disabled
2. Try private/incognito mode (fresh storage)
3. Check browser settings for LocalStorage permissions
4. Try different browser

---

## 📋 Feature Checklist

- ✅ Run simulations
- ✅ Auto-save each simulation
- ✅ Simulations numbered (1, 2, 3...)
- ✅ Load previous simulations
- ✅ Delete unwanted simulations
- ✅ View saved simulations list
- ✅ Compare energy across simulations
- ✅ Compare fairness across simulations
- ✅ Side-by-side metrics table
- ✅ All KPI cards populate
- ✅ All charts render
- ✅ All tables show data
- ✅ Strategy section has data
- ✅ Fairness section has data
- ✅ Experiments section tracks runs
- ✅ Logs section shows data
- ✅ Persistent storage (LocalStorage)
- ✅ Comparison charts interactive (hover, legend, zoom)

---

## 🎊 Success Indicators

**Dashboard is working correctly when**:

✅ After running a simulation:
- KPI cards show actual numbers (not 0.00)
- All 4 dashboard charts render with data
- Results table shows round-by-round data

✅ Strategy Comparison section:
- Bar chart shows 3 strategies
- Radar chart shows metrics
- Table has rows of data

✅ Fairness section:
- Heatmap visible
- Carbon timeline shows data
- Energy mix pie chart displays
- Fairness vs Energy scatter shows points

✅ Experiments section:
- Table shows your simulation
- Energy comparison chart renders
- Fairness comparison chart renders

✅ Compare Sims section (after 2+ simulations):
- Saved simulations list shows entries
- Energy comparison chart shows bars
- Fairness comparison chart shows bars
- Comparison table lists all simulations

✅ Logs section:
- Simulation log shows text details
- Raw data shows JSON

**If all ✅**: Your dashboard is fully functional! 🎉

---

## 📞 Quick Reference

| Task | Where | How |
|------|-------|-----|
| Run simulation | Node Configuration | Click Execute Simulation |
| Save simulation | Auto | Saved when simulation completes |
| Compare simulations | Compare Sims section | Auto-displayed (2+ sims needed) |
| Load previous sim | Compare Sims (left panel) | Click simulation name |
| Delete simulation | Compare Sims (table) | Click 🗑️ button |
| View strategy data | Strategy Comparison | Auto-populated after sim |
| View fairness data | Fairness & Carbon | Auto-populated after sim |
| View experiments | Experiments | Auto-populated after sim |
| View logs | Logs & Export | Auto-populated after sim |
| Export data | Logs & Export | Click Export CSV/JSON |

---

## 🎓 Best Practices

1. **Run multiple simulations** with different parameters to see differences
2. **Use comparison section** to find best strategy
3. **Save important simulations** by not deleting them
4. **Export data** for reports and analysis
5. **Check all sections** after each simulation to verify data

---

**Version**: v3.1 with Simulation Save & Compare  
**Status**: ✅ Production Ready  
**Last Updated**: January 22, 2026

