#!/usr/bin/env node
/**
 * GENERATE ETERNAL DASHBOARD
 * 
 * Creates markdown files with embedded HTML dashboards
 * that render directly in Cursor's preview pane
 * No server needed - pure file-based, eternal, local
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
 */

const fs = require('fs');
const path = require('path');

const workspaceRoot = path.resolve(__dirname, '..');
const sourceOfTruthPath = path.join(workspaceRoot, '.ai-context-source-of-truth.json');
const dashboardMarkdownPath = path.join(workspaceRoot, 'DRIFT_DASHBOARD_ETERNAL.md');
const dashboardHtmlPath = path.join(workspaceRoot, 'drift-dashboard-eternal.html');

function generateEternalDashboard() {
  // Read AI context source of truth
  let data = {};
  if (fs.existsSync(sourceOfTruthPath)) {
    try {
      data = JSON.parse(fs.readFileSync(sourceOfTruthPath, 'utf8'));
    } catch (err) {
      console.error('Error reading source of truth:', err.message);
      return;
    }
  }

  // Generate HTML dashboard
  const html = generateDashboardHTML(data);
  
  // Write standalone HTML file (for Cursor preview)
  fs.writeFileSync(dashboardHtmlPath, html, 'utf8');
  
  // Create markdown file with iframe reference
  const markdown = `# 🛡️ DRIFT PROTECTION DASHBOARD - ETERNAL

**Last Updated**: ${new Date().toLocaleString()}  
**Status**: ✅ **LIVE - AUTO-UPDATING**  
**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE

---

## 📊 HOW TO USE IN CURSOR

### Option 1: HTML Preview (Recommended)
1. **Open** \`drift-dashboard-eternal.html\` in Cursor
2. **Right-click** → "Open Preview" or press \`Cmd+Shift+V\`
3. **Pin the tab** for always-visible dashboard
4. Dashboard **auto-updates** when source changes

### Option 2: Markdown Preview
1. **Open** this file (\`DRIFT_DASHBOARD_ETERNAL.md\`) in Cursor
2. **Open preview**: \`Cmd+Shift+V\` (Mac) or \`Ctrl+Shift+V\` (Windows/Linux)
3. Dashboard loads in iframe below

---

## 🔄 AUTO-UPDATE SETUP

Run this to enable auto-updates:

\`\`\`bash
node scripts/watch-eternal-dashboard.js
\`\`\`

Dashboard regenerates automatically on every change to \`.ai-context-source-of-truth.json\`

---

## 📊 LIVE DASHBOARD

<iframe src="drift-dashboard-eternal.html" width="100%" height="800px" frameborder="0" style="border: 2px solid #3e3e42; border-radius: 8px;"></iframe>

---

## ✅ ETERNAL FEATURES

- ✅ **Pure file-based** - No server needed
- ✅ **Auto-updates** - Regenerates on data changes
- ✅ **Works in Cursor** - Opens in preview pane
- ✅ **Eternal** - Persists across sessions
- ✅ **Local** - All data stays local

---

**Pattern**: OBSERVER × TRUTH × ATOMIC × ONE  
**Status**: ✅ **ETERNAL DASHBOARD ACTIVE**  
∞ AbëONE ∞
`;

  // Write markdown file
  fs.writeFileSync(dashboardMarkdownPath, markdown, 'utf8');
  console.log(`✅ Generated eternal dashboard:`);
  console.log(`   - HTML: ${dashboardHtmlPath}`);
  console.log(`   - Markdown: ${dashboardMarkdownPath}`);
}

function generateErrorDashboard(message) {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #1e1e1e;
  color: #cccccc;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
.error-container {
  text-align: center;
  padding: 40px;
  background: #252526;
  border-radius: 8px;
  border: 2px solid #f48771;
}
.error-icon { font-size: 48px; margin-bottom: 20px; }
.error-message {
  font-size: 18px;
  color: #f48771;
  margin-bottom: 10px;
}
.error-details {
  font-size: 14px;
  color: #858585;
  margin-top: 10px;
}
</style>
</head>
<body>
<div class="error-container">
  <div class="error-icon">⚠️</div>
  <div class="error-message">SUBSTRATE-REQUIRED: ${message}</div>
  <div class="error-details">Dashboard data unavailable. Check source of truth file.</div>
</div>
</body>
</html>`;
}

function generateDashboardHTML(data) {
  // SUBSTRATE-REQUIRED: Validate data structure before accessing
  if (!data) {
    console.warn('SUBSTRATE-REQUIRED: Missing data in source of truth');
    return generateErrorDashboard('Missing data in source of truth');
  }
  
  // Require substrate - don't mask with defaults
  const systemStatus = data.systemStatus;
  const workspace = data.workspace;
  const projects = data.projects;
  
  // Validate substrate exists
  if (!systemStatus) {
    console.warn('SUBSTRATE-REQUIRED: Missing systemStatus in source of truth');
    return generateErrorDashboard('Missing systemStatus - data unavailable');
  }
  
  if (!workspace) {
    console.warn('SUBSTRATE-REQUIRED: Missing workspace in source of truth');
    return generateErrorDashboard('Missing workspace - data unavailable');
  }
  
  if (!projects) {
    console.warn('SUBSTRATE-REQUIRED: Missing projects in source of truth');
    return generateErrorDashboard('Missing projects - data unavailable');
  }
  
  // Use nullish coalescing for explicit defaults (not masking)
  const healthScore = systemStatus.overallHealth ?? null;
  const criticalIssues = systemStatus.criticalIssues ?? null;
  const warnings = systemStatus.warnings ?? null;
  
  // If critical data missing, show error instead of false metrics
  if (healthScore === null || criticalIssues === null || warnings === null) {
    return generateErrorDashboard('Incomplete system status data');
  }
  
  // Embed data directly in HTML to avoid CORS issues
  const embeddedData = JSON.stringify(data);
  
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #1e1e1e;
  color: #cccccc;
  padding: 20px;
  font-size: 13px;
}
.container { max-width: 100%; }
.header {
  text-align: center;
  padding: 20px;
  background: #252526;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 2px solid #3e3e42;
}
.header h1 {
  font-size: 24px;
  color: #4ec9b0;
  margin-bottom: 10px;
}
.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #4ec9b0;
  animation: pulse 2s infinite;
  margin-left: 8px;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}
.card {
  background: #252526;
  border-radius: 8px;
  padding: 15px;
  border: 2px solid #3e3e42;
}
.card-header {
  font-size: 16px;
  font-weight: bold;
  color: #4ec9b0;
  margin-bottom: 12px;
  border-bottom: 1px solid #3e3e42;
  padding-bottom: 8px;
}
.metric-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #3e3e42;
}
.metric-row:last-child { border-bottom: none; }
.metric-label { color: #858585; }
.metric-value {
  font-weight: bold;
  color: #4ec9b0;
}
.score-bar {
  margin-top: 10px;
  height: 8px;
  background: #3e3e42;
  border-radius: 4px;
  overflow: hidden;
}
.score-fill {
  height: 100%;
  background: ${healthScore >= 80 ? '#4ec9b0' : healthScore >= 50 ? '#f48771' : '#f48771'};
  transition: width 0.5s ease;
  border-radius: 4px;
  width: ${healthScore}%;
}
.project-item {
  padding: 10px;
  margin: 8px 0;
  background: #1e1e1e;
  border-radius: 6px;
  border-left: 3px solid #4ec9b0;
}
.project-name {
  font-weight: bold;
  margin-bottom: 4px;
}
.project-status {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 3px;
  background: #3e3e42;
  color: #4ec9b0;
  display: inline-block;
}
.action-item {
  padding: 10px;
  margin: 6px 0;
  background: #3a2e1e;
  border-radius: 6px;
  border-left: 3px solid #f48771;
}
.action-priority {
  font-size: 11px;
  color: #f48771;
  font-weight: bold;
  margin-bottom: 4px;
}
.action-text { font-size: 12px; }
.action-command {
  font-size: 10px;
  color: #569cd6;
  font-family: 'Courier New', monospace;
  background: #1e1e1e;
  padding: 4px 8px;
  border-radius: 4px;
  margin-top: 4px;
  display: inline-block;
}
.last-updated {
  text-align: center;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #3e3e42;
  font-size: 11px;
  color: #858585;
}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🛡️ Drift Protection Dashboard<span class="status-indicator"></span></h1>
    <div style="font-size: 12px; color: #858585;">Real-time monitoring • Auto-updating</div>
  </div>
  
  <div class="grid">
    <div class="card">
      <div class="card-header">📊 System Health</div>
      <div class="metric-row">
        <span class="metric-label">Overall Health</span>
        <span class="metric-value health-score">${healthScore}%</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Critical Issues</span>
        <span class="metric-value critical-count" style="color: ${criticalIssues > 0 ? '#f48771' : '#4ec9b0'}">${criticalIssues}</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Warnings</span>
        <span class="metric-value warnings-count" style="color: #f48771">${warnings}</span>
      </div>
      <div class="score-bar health-bar">
        <div class="score-fill" style="width: ${healthScore}%"></div>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">📦 Current Project</div>
      <div class="project-item">
        <div class="project-name current-project-name">${workspace.currentProject || 'Workspace Root'}</div>
        <div class="current-project-dir" style="font-size: 11px; color: #858585; margin-top: 4px;">
          ${workspace.currentDirectory || workspace.root || 'N/A'}
        </div>
      </div>
    </div>
    
    <div class="card">
      <div class="card-header">✨ Active Projects</div>
      <div class="projects-list">
      ${(projects.active || []).slice(0, 3).map(project => {
        const score = project.operationalStatus?.score || 0;
        const status = project.operationalStatus?.status || project.status || 'UNKNOWN';
        return `
        <div class="project-item">
          <div class="project-name">
            ${project.name}
            <span class="project-status">${status}</span>
          </div>
          <div style="font-size: 10px; color: #858585; margin-top: 4px;">${project.directory}</div>
          <div class="score-bar" style="margin-top: 6px; height: 4px;">
            <div class="score-fill" style="width: ${score}%"></div>
          </div>
        </div>`;
      }).join('')}
      </div>
    </div>
  </div>
  
  ${systemStatus.criticalActions && systemStatus.criticalActions.length > 0 ? `
  <div class="card">
    <div class="card-header">🚨 Critical Actions</div>
    <div class="actions-list">
    ${systemStatus.criticalActions.slice(0, 3).map(action => `
      <div class="action-item">
        <div class="action-priority">${action.priority}</div>
        <div class="action-text">${action.action}</div>
        ${action.command ? `<div class="action-command">${action.command}</div>` : ''}
      </div>
    `).join('')}
    </div>
  </div>
  ` : '<div class="card"><div class="card-header">🚨 Critical Actions</div><div class="actions-list"><div style="padding: 10px; color: #858585;">No critical actions</div></div></div>'}
  
  <div class="last-updated">
    Last updated: <span class="last-updated-time">${new Date().toLocaleString()}</span>
  </div>
</div>

<script>
// ETERNAL: Use embedded data + fetch for updates
let lastData = null;
let updateCount = 0;
const embeddedData = ${embeddedData};

// Load embedded data first
if (embeddedData) {
  lastData = JSON.stringify(embeddedData);
  renderDashboard(embeddedData);
  updateLastUpdated();
}

async function loadDashboardData() {
  try {
    // Try to fetch updated data (works if served via HTTP, falls back to embedded if file://)
    try {
      const response = await fetch('.ai-context-source-of-truth.json?t=' + Date.now());
      if (response.ok) {
        const data = await response.json();
        updateIfChanged(data);
        return;
      }
    } catch (fetchError) {
      // File:// protocol - use embedded data
      if (embeddedData) {
        updateIfChanged(embeddedData);
      }
      return;
    }
  } catch (error) {
    // Use embedded data as fallback
    if (embeddedData) {
      updateIfChanged(embeddedData);
    }
  }
}

function updateIfChanged(data) {
  const dataStr = JSON.stringify(data);
  if (dataStr !== lastData) {
    lastData = dataStr;
    updateCount++;
    renderDashboard(data);
    updateLastUpdated();
  }
}

function renderDashboard(data) {
  // SUBSTRATE-REQUIRED: Validate data structure
  if (!data || !data.systemStatus || !data.workspace || !data.projects) {
    console.error('SUBSTRATE-REQUIRED: Missing data in dashboard render');
    return;
  }
  
  const systemStatus = data.systemStatus;
  const workspace = data.workspace;
  const projects = data.projects;
  
  // Use nullish coalescing for explicit defaults (not masking)
  const healthScore = systemStatus.overallHealth ?? null;
  const criticalIssues = systemStatus.criticalIssues ?? null;
  const warnings = systemStatus.warnings ?? null;
  
  // If critical data missing, don't render false metrics
  if (healthScore === null || criticalIssues === null || warnings === null) {
    console.error('SUBSTRATE-REQUIRED: Incomplete system status data');
    return;
  }
  
  // Update system health
  document.querySelector('.health-score').textContent = healthScore + '%';
  document.querySelector('.health-bar .score-fill').style.width = healthScore + '%';
  document.querySelector('.critical-count').textContent = criticalIssues;
  document.querySelector('.warnings-count').textContent = warnings;
  
  // Update current project
  document.querySelector('.current-project-name').textContent = workspace.currentProject || 'Workspace Root';
  document.querySelector('.current-project-dir').textContent = workspace.currentDirectory || workspace.root || 'N/A';
  
  // Update projects list
  const projectsContainer = document.querySelector('.projects-list');
  if (projectsContainer) {
    projectsContainer.innerHTML = (projects.active || []).slice(0, 3).map(project => {
      const score = project.operationalStatus?.score || 0;
      const status = project.operationalStatus?.status || project.status || 'UNKNOWN';
      return \`
        <div class="project-item">
          <div class="project-name">
            \${project.name}
            <span class="project-status">\${status}</span>
          </div>
          <div style="font-size: 10px; color: #858585; margin-top: 4px;">\${project.directory}</div>
          <div class="score-bar" style="margin-top: 6px; height: 4px;">
            <div class="score-fill" style="width: \${score}%; background: \${score >= 80 ? '#4ec9b0' : score >= 50 ? '#f48771' : '#f48771'}"></div>
          </div>
        </div>
      \`;
    }).join('');
  }
  
  // Update critical actions
  const actionsContainer = document.querySelector('.actions-list');
  if (actionsContainer && systemStatus.criticalActions) {
    actionsContainer.innerHTML = systemStatus.criticalActions.slice(0, 3).map(action => \`
      <div class="action-item">
        <div class="action-priority">\${action.priority}</div>
        <div class="action-text">\${action.action}</div>
        \${action.command ? \`<div class="action-command">\${action.command}</div>\` : ''}
      </div>
    \`).join('');
  }
}

function updateLastUpdated() {
  const element = document.querySelector('.last-updated-time');
  if (element) {
    element.textContent = new Date().toLocaleString();
  }
}

// Load immediately
loadDashboardData();

// Auto-refresh every 2 seconds (ETERNAL - reads directly from JSON)
setInterval(loadDashboardData, 2000);

// Also refresh when tab becomes visible
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    loadDashboardData();
  }
});
</script>
</body>
</html>`;
}

// Run if called directly
if (require.main === module) {
  generateEternalDashboard();
}

/**
 * Generate error dashboard when substrate is missing
 */
function generateErrorDashboard(message) {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #1e1e1e;
  color: #cccccc;
  padding: 20px;
  font-size: 13px;
}
.error-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  background: #252526;
  border-radius: 8px;
  border: 2px solid #f48771;
  text-align: center;
}
.error-title {
  font-size: 24px;
  color: #f48771;
  margin-bottom: 15px;
}
.error-message {
  color: #858585;
  margin-bottom: 20px;
}
.success-actions {
  text-align: left;
  background: #1e1e1e;
  padding: 15px;
  border-radius: 6px;
  margin-top: 20px;
}
.success-actions h3 {
  color: #4ec9b0;
  margin-bottom: 10px;
}
.success-actions ol {
  color: #858585;
  padding-left: 20px;
}
.success-actions li {
  margin: 8px 0;
}
</style>
</head>
<body>
  <div class="error-container">
    <div class="error-title">SUBSTRATE-REQUIRED</div>
    <div class="error-message">${message}</div>
    <div class="success-actions">
      <h3>To fix:</h3>
      <ol>
        <li>Provide missing data using exact substrate.</li>
        <li>Re-run command with updated context.</li>
        <li>Lock file or status block regenerates automatically from substrate.</li>
        <li>System revalidates and converges to correct state.</li>
      </ol>
    </div>
  </div>
</body>
</html>`;
}

module.exports = { generateEternalDashboard };

