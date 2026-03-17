# 🧪 Dashboard Testing Guide - Step by Step

**Current Status**: Dashboard running at http://localhost:5000

---

## ⚠️ Why You See Empty Results

The simulation results are **empty on first load** because:
- No nodes have been configured yet
- No simulation has been executed
- Dashboard loads but waits for data

**Solution**: Follow this step-by-step process to populate data.

---

## 🎯 Complete Testing Process

### **STEP 1: Navigate to Node Configuration**

**Where**: http://localhost:5000

**What to do**:
1. Look at the **left sidebar** (dark panel with menu items)
2. Click on **"🖥️ Node Configuration"** (2nd menu item)
3. You'll see a form on the left side with fields

---

### **STEP 2: Add Your First Node**

**Where**: Node Configuration section (right side of form)

**Form fields to fill**:
```
Node Type:     [Dropdown] → Select "Edge Device"
CPU (cores):   [Input]    → Enter "4"
Memory (GB):   [Input]    → Enter "8"
Energy (W):    [Input]    → Enter "50"
SLA Target:    [Input]    → Enter "0.95"
Region:        [Dropdown] → Select "US-East"
```

**After filling form**:
- Click blue **"➕ Add Node"** button
- Wait 1-2 seconds
- You'll see node appear in the table below the form

**Example**: After click, you should see:
```
ID | Type | CPU | Memory | Energy | SLA | Region | Action
1  | Edge | 4   | 8      | 50     | 0.95| US-East | ❌
```

---

### **STEP 3: Add 3-5 More Nodes**

**Why**: Simulations need multiple nodes to show meaningful results

**Repeat Step 2**, but add different configurations:

**Node 2**:
- Type: Cloud Server
- CPU: 8
- Memory: 16
- Energy: 100
- SLA: 0.98
- Region: EU-West

**Node 3**:
- Type: Fog Node
- CPU: 2
- Memory: 4
- Energy: 25
- SLA: 0.90
- Region: APAC

**Node 4**:
- Type: Edge Device
- CPU: 6
- Memory: 12
- Energy: 60
- SLA: 0.95
- Region: US-West

**Result**: Your node table should show 4 nodes listed

---

### **STEP 4: Run Your First Simulation**

**Where**: Still in Node Configuration section (scroll down)

**What you'll see**:
- Section titled **"Run Custom Simulation"**
- Field: **"Optimization Target"** (dropdown)
- Field: **"Rounds"** (number input)
- Blue button: **"▶️ Run Simulation"**

**How to run**:

1. **Select optimization target**:
   - Click dropdown → choose "Energy Efficiency"

2. **Set number of rounds**:
   - Click input field → enter "10"

3. **Execute**:
   - Click **"▶️ Run Simulation"** button

4. **Wait for completion**:
   - Server will process (takes 5-30 seconds)
   - You'll see progress in browser console (F12 → Console tab)
   - Status will appear: "Simulation completed!" or similar

---

### **STEP 5: View Dashboard Results**

**Where**: Click **"🏠 Dashboard"** (1st menu item) in sidebar

**What you should now see**:

**Top Row - 6 KPI Cards**:
```
┌──────────────┬──────────────┬──────────────┐
│ Total Energy │ Avg SLA      │ Fairness     │
│ 234 kWh ↓    │ 0.94 ✓       │ 0.82 ↓       │
├──────────────┼──────────────┼──────────────┤
│ Carbon       │ Active Nodes │ Best Strategy│
│ 156 kg CO₂ ↓ │ 4 ✓          │ Energy Eff.  │
└──────────────┴──────────────┴──────────────┘
```

**Numbers will be FILLED with actual data** ✓

---

### **STEP 6: Check Charts on Dashboard**

**Location**: Below KPI cards (4 main charts)

**Chart 1 - Loss Convergence**:
- Shows line graph going down
- X-axis: Rounds (1-10)
- Y-axis: Loss value
- Should show decreasing trend ✓

**Chart 2 - Resource Utilization**:
- Shows stacked area
- CPU, Memory, Disk over rounds
- Should show resource patterns ✓

**Chart 3 - Metric Distribution**:
- Pie/donut chart
- Shows metric percentages
- Should show split of metrics ✓

**Chart 4 - Client Performance**:
- Bar chart
- Each node's performance
- Should show 4 bars (one per node) ✓

---

### **STEP 7: Check Simulation Results Table**

**Location**: Below the 4 charts on Dashboard

**Table columns**:
```
Round | Avg Loss | Energy | SLA   | Fairness | Carbon
------|----------|--------|-------|----------|--------
1     | 0.85     | 234    | 0.92  | 0.80     | 156
2     | 0.78     | 220    | 0.93  | 0.81     | 150
...   | ...      | ...    | ...   | ...      | ...
10    | 0.45     | 180    | 0.94  | 0.84     | 120
```

**Should show**: 10 rows (one per round) with real numbers ✓

---

### **STEP 8: Explore Analytics Section**

**Where**: Click **"📈 Federated Analytics"** in sidebar

**What to do**:
1. You'll see **Round Slider** at top
2. Drag slider from 1 to 10
3. You'll see 6 different charts:
   - Multi-line (Loss vs Resources)
   - Client Heatmap
   - Box Plot
   - Scatter Plot
   - Histogram
   - Radar Chart

**All should populate with data** ✓

---

### **STEP 9: Check Strategy Comparison**

**Where**: Click **"⚖️ Strategy Comparison"** in sidebar

**What to do**:
1. You'll see **checkboxes** for metrics (Energy, SLA, Fairness, etc.)
2. Check 2-3 checkboxes
3. Click any checkbox to toggle chart updates
4. You'll see:
   - **Grouped bar chart** comparing strategies
   - **Radar chart** showing metrics

**Charts should update dynamically** ✓

---

### **STEP 10: Test Export Function**

**Where**: Click **"📁 Logs & Export"** in sidebar

**What to do**:
1. Scroll to **"Export Options"** section
2. Click **"📥 Export CSV"** button
3. File downloads to your computer
4. Open it in Excel/notepad - should contain all simulation data

**OR**:
1. Click **"📥 Export JSON"** button
2. File downloads with full simulation object
3. Open in text editor - valid JSON format

---

## 🔍 Where to Check for Problems

### **If Dashboard is Empty**:

**Problem**: No data showing, all cards empty

**Solution**:
1. Open browser console: **F12** → **Console** tab
2. Look for errors (red text)
3. Check if simulation completed: look for "Simulation completed!" message
4. Try running simulation again

### **If Charts Don't Render**:

**Problem**: Chart containers show but no lines/bars

**Solution**:
1. Press **F12** → **Network** tab
2. Run simulation again
3. Look for POST request to `/api/simulation/start`
4. Check if response is 200 OK
5. If error, check Flask server terminal for error messages

### **If Node Creation Fails**:

**Problem**: Node doesn't appear in table after clicking Add

**Solution**:
1. Check all form fields are filled
2. Check browser console for error messages
3. Check Flask server terminal output
4. Try clearing all nodes: **"🗑️ Clear All"** button
5. Then add fresh nodes

---

## 📋 Complete Testing Checklist

Use this checklist to verify everything works:

- [ ] Dashboard loads at http://localhost:5000
- [ ] Sidebar visible with 8 menu items
- [ ] Can navigate between sections (no errors)
- [ ] Add node form works (node appears in table)
- [ ] Can add 4+ nodes successfully
- [ ] Run Simulation button works
- [ ] Simulation completes (5-30 seconds)
- [ ] Dashboard KPI cards show numbers
- [ ] All 4 dashboard charts render
- [ ] Results table shows 10 rows
- [ ] Analytics section shows 6 charts
- [ ] Strategy charts render
- [ ] Export CSV downloads file
- [ ] Export JSON downloads file
- [ ] Sidebar collapse/expand works
- [ ] Mobile responsive (resize browser to 375px)
- [ ] No red errors in browser console (F12)

**All checked?** ✅ **Dashboard is working perfectly!**

---

## 🎮 Interactive Testing Scenarios

### **Scenario 1: Quick Test (5 minutes)**

1. Add 2 nodes (Edge Device + Cloud Server)
2. Run simulation (10 rounds, Energy Efficiency)
3. Check Dashboard KPI cards
4. Check one chart (Loss Convergence)
5. Done!

### **Scenario 2: Full Test (15 minutes)**

1. Add 4 nodes (different types/regions)
2. Run simulation (20 rounds, SLA Optimization)
3. Check Dashboard (all 4 charts)
4. Check Analytics (all 6 charts)
5. Check Strategy Comparison
6. Export to CSV
7. Test responsive design (resize window)

### **Scenario 3: Stress Test (30 minutes)**

1. Add 10 nodes (various configurations)
2. Run 3 simulations (different targets)
3. Verify all sections populate
4. Test all export options
5. Check mobile/tablet/desktop views
6. Test sidebar collapse on mobile
7. Verify performance (no lag)

---

## 🐛 Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Empty cards on Dashboard | No simulation run | Run simulation from Step 4 |
| Charts show "No data" | Data not loaded | Wait for simulation to complete, check console |
| Node won't add | Form incomplete | Fill all 6 fields, check dropdown values |
| Simulation takes too long | Server busy | Wait 30 seconds, try again |
| Export button does nothing | File download blocked | Check browser download settings |
| Sidebar won't collapse | CSS issue | Refresh page (F5) |
| Charts look wrong on mobile | Responsive issue | This is normal - resize to see proper layout |

---

## 📊 What Data Should Look Like

### **After Running 1 Simulation with 4 Nodes, 10 Rounds**:

**KPI Cards**:
- Total Energy: 1,200-2,000 kWh
- Avg SLA: 0.90-0.98
- Fairness: 0.75-0.95
- Carbon: 800-1,300 kg CO₂
- Active Nodes: 4
- Best Strategy: "Energy Efficiency" or similar

**Loss Chart**:
- Starts high (0.8-0.9)
- Ends low (0.3-0.5)
- Downward trend over 10 rounds

**Resource Chart**:
- Shows 3 stacked areas (CPU, Memory, Disk)
- Values between 0-100 per resource

**Metrics Chart**:
- Pie splits into 4-5 segments
- Each segment 10-40% of total

**Client Chart**:
- 4 bars (one per node)
- Heights 60-100 units each

---

## ✨ Pro Tips

1. **Multiple Simulations**: Run same simulation twice - data should accumulate
2. **Different Parameters**: Change optimization target to see different results
3. **Export & Analyze**: Export CSV, open in Excel to see full data
4. **Mobile Testing**: Resize browser to 375px to test phone layout
5. **Performance**: Check browser Network tab to see API response times
6. **Dark Theme**: Works best in dark room or with dark monitor settings

---

## 🎯 Success Indicators

**Dashboard is working correctly when**:

✅ KPI cards show actual numbers (not 0 or N/A)  
✅ Charts have visible lines/bars/shapes  
✅ Results table shows 10 rows  
✅ No red errors in console (F12)  
✅ Export buttons download files  
✅ Navigation smooth and fast  
✅ Sidebar collapses on click  
✅ Mobile view is responsive  

**If all ✅**: **Your dashboard is production-ready!** 🚀

---

## 📞 Troubleshooting Flowchart

```
Start Testing
    ↓
Navigate to http://localhost:5000
    ↓
Add 4 nodes in Node Configuration
    ↓
Run Simulation (10 rounds)
    ↓
→ Simulation fails?
    └─ Check Flask terminal for error
    └─ Open F12 console for JS errors
    └─ Restart Flask server
    └─ Try again
    ↓
→ Simulation succeeds
    ↓
Go to Dashboard
    ↓
→ KPI cards empty?
    └─ Simulation didn't finish
    └─ Check console for "Simulation completed!"
    └─ Wait 30 seconds and refresh
    ↓
→ KPI cards show numbers? ✅
    ↓
Check charts render
    ↓
→ Charts show data? ✅
    ↓
Test other sections (Analytics, Strategy)
    ↓
→ All working? ✅
    ↓
Test Export
    ↓
→ Files download? ✅
    ↓
TESTING COMPLETE ✅
```

---

## 📌 Quick Reference

**Server**: http://localhost:5000  
**F12 Console**: For debugging (Press F12 → Console tab)  
**Flask Terminal**: Shows API requests and errors  
**First Step**: Add nodes in "Node Configuration" section  
**Second Step**: Run simulation with "Run Simulation" button  
**Third Step**: View results in "Dashboard" section  
**Export**: Go to "Logs & Export" section  

---

**Remember**: Empty results are normal on first load. You must follow steps 1-7 to populate data. After that, all sections should show real simulation results! 🎉
