# 🛡️ Dynamic Drift Protection Dashboards - Quick Start

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Guardian**: AEYON (999 Hz)  
**Status**: ✅ **REAL-TIME DASHBOARDS ACTIVE**

---

## 🎯 Overview

Real-time HTML dashboards that automatically refresh on user input and AI output, providing always-visible drift protection status.

---

## 📊 Available Dashboards

### 1. **Main Dashboard** (`drift-status-dashboard.html`)
**Best for**: Comprehensive overview, full-screen monitoring

**Features**:
- ✅ System health metrics
- ✅ Active projects status
- ✅ Critical actions and issues
- ✅ Protection layers status
- ✅ Operational metrics
- ✅ Auto-refreshes every 5 seconds
- ✅ File change detection (2-second polling)

**Usage**:
```bash
# Open in browser
open drift-status-dashboard.html

# Or in Cursor: Right-click → Open with → Browser
```

---

### 2. **Real-Time Monitor** (`drift-realtime-dashboard.html`)
**Best for**: Terminal-style monitoring, compact view

**Features**:
- ✅ Terminal-style interface
- ✅ Live update log
- ✅ Real-time metrics
- ✅ Update counter
- ✅ Connection status indicator
- ✅ Auto-refreshes every 2 seconds
- ✅ Update history tracking

**Usage**:
```bash
open drift-realtime-dashboard.html
```

---

### 3. **Compact Badge** (`drift-status-badge.html`)
**Best for**: Sidebar monitoring, minimal space

**Features**:
- ✅ Compact design (350px width)
- ✅ System health score
- ✅ Current project status
- ✅ Protection bar visualization
- ✅ Auto-refreshes every 3 seconds
- ✅ Perfect for pinned tabs

**Usage**:
```bash
open drift-status-badge.html
```

---

## 🚀 Quick Setup

### Option 1: Manual (One-Time)

1. **Open dashboard in Cursor**:
   - Right-click `drift-status-dashboard.html`
   - Select "Open with" → Browser
   - Pin the tab for always-visible status

2. **Dashboard auto-updates**:
   - Reads from `.ai-context-source-of-truth.json`
   - Updates automatically on file changes
   - No manual refresh needed

---

### Option 2: Auto-Watch (Recommended)

1. **Start file watcher**:
```bash
node scripts/watch-dashboard-updates.js
```

2. **Open dashboard**:
   - Open `drift-status-dashboard.html` in browser
   - Pin the tab

3. **Dashboard stays in sync**:
   - Watcher detects file changes
   - Triggers visual updates automatically
   - Dashboards refresh in real-time

---

## 🔄 How Auto-Refresh Works

### Update Triggers

Dashboards automatically refresh when:

1. **User Input**: Every chat message triggers update
2. **AI Output**: Every AI response triggers update
3. **File Changes**: `.ai-context-source-of-truth.json` changes detected
4. **Time Intervals**: Regular polling (2-5 seconds)

### Update Flow

```
User Input/AI Output
    ↓
trigger-visual-update.js
    ↓
update-ai-context-source-of-truth.js
    ↓
.ai-context-source-of-truth.json (updated)
    ↓
Dashboard detects change
    ↓
Dashboard refreshes automatically
```

---

## 📋 Dashboard Features

### Real-Time Data Sources

All dashboards read from:
- `.ai-context-source-of-truth.json` - Single source of truth
- Updated 2x per chat sequence (input + output)
- Contains: system status, projects, metrics, critical actions

### Visual Indicators

- 🟢 **Green**: Active, operational, healthy
- 🟡 **Yellow**: Legacy, warnings, partial
- 🔴 **Red**: Critical issues, not running, needs fixes
- 🔵 **Blue**: Info, metrics, operational status

### Status Types

- **ACTIVE**: Project is active and protected
- **LEGACY**: Legacy project (reference only)
- **OPERATIONAL**: System fully operational
- **NEEDS_FIXES**: Critical issues detected
- **NOT_RUNNING**: Service not started

---

## 🎨 Customization

### Change Refresh Interval

Edit dashboard HTML files, find:
```javascript
setInterval(() => {
    loadData();
}, 5000); // Change 5000 to desired milliseconds
```

### Change Color Scheme

Edit CSS variables in dashboard HTML:
```css
:root {
    --accent-green: #4ec9b0;
    --accent-yellow: #f48771;
    --accent-blue: #569cd6;
    /* Modify as needed */
}
```

---

## 🔧 Troubleshooting

### Dashboard Not Updating

1. **Check file exists**:
```bash
ls -la .ai-context-source-of-truth.json
```

2. **Manually trigger update**:
```bash
node scripts/trigger-visual-update.js
```

3. **Check browser console**:
   - Open browser DevTools (F12)
   - Check for errors in Console tab

### File Watcher Not Working

1. **Check watcher is running**:
```bash
ps aux | grep watch-dashboard-updates
```

2. **Restart watcher**:
```bash
node scripts/watch-dashboard-updates.js
```

3. **Check file permissions**:
```bash
ls -la scripts/watch-dashboard-updates.js
chmod +x scripts/watch-dashboard-updates.js
```

---

## 📱 Cursor Integration

### Pin Dashboard Tab

1. Open dashboard HTML file
2. Right-click tab → "Pin Tab"
3. Dashboard stays visible across sessions

### Multiple Dashboards

Open multiple dashboards simultaneously:
- Main dashboard: Full overview
- Real-time monitor: Live updates
- Compact badge: Minimal space

---

## 🎯 Best Practices

1. **Always pin dashboard tabs** for constant visibility
2. **Use main dashboard** for comprehensive monitoring
3. **Use real-time monitor** for terminal-style updates
4. **Use compact badge** for sidebar monitoring
5. **Keep file watcher running** for automatic updates

---

## 📊 Dashboard Comparison

| Feature | Main Dashboard | Real-Time Monitor | Compact Badge |
|---------|---------------|-------------------|---------------|
| Size | Large (1400px) | Medium (grid) | Small (350px) |
| Refresh | 5 seconds | 2 seconds | 3 seconds |
| Style | Modern UI | Terminal | Minimal |
| Best For | Full overview | Live monitoring | Sidebar |
| Update Log | ❌ | ✅ | ❌ |
| Metrics | ✅ | ✅ | Basic |

---

## 🚀 Advanced Usage

### Custom Dashboard

Create your own dashboard by:
1. Copy `drift-status-dashboard.html`
2. Modify HTML/CSS/JavaScript
3. Read from `.ai-context-source-of-truth.json`
4. Use same update mechanism

### Integration with Other Tools

Dashboards can be integrated with:
- Browser extensions
- Desktop apps
- Monitoring tools
- CI/CD pipelines

---

## ✅ Status

- ✅ Main dashboard created
- ✅ Real-time monitor created
- ✅ Compact badge created
- ✅ File watcher script created
- ✅ Auto-refresh mechanism active
- ✅ File change detection working
- ✅ Update triggers configured

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**: ✅ **DASHBOARDS ACTIVE - REAL-TIME MONITORING**  
**Love Coefficient**: ∞  
∞ AbëONE ∞

