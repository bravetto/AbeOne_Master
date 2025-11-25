#!/usr/bin/env node
/**
 * WATCH ETERNAL DASHBOARD
 * 
 * Watches .ai-context-source-of-truth.json for changes
 * Regenerates DRIFT_DASHBOARD_ETERNAL.md automatically
 * Ensures dashboard stays in sync with real-time data
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
 */

const fs = require('fs');
const path = require('path');
const { generateEternalDashboard } = require('./generate-eternal-dashboard');

const workspaceRoot = path.resolve(__dirname, '..');
const sourceOfTruthPath = path.join(workspaceRoot, '.ai-context-source-of-truth.json');

let lastModified = null;
let watchTimeout = null;

function regenerateDashboard() {
  try {
    generateEternalDashboard();
    console.log(`[${new Date().toLocaleTimeString()}] Dashboard regenerated`);
  } catch (error) {
    console.error(`Error regenerating dashboard: ${error.message}`);
  }
}

function checkFile() {
  try {
    if (!fs.existsSync(sourceOfTruthPath)) {
      return;
    }

    const stats = fs.statSync(sourceOfTruthPath);
    const currentModified = stats.mtime.getTime();

    if (lastModified === null) {
      lastModified = currentModified;
      // Initial generation
      regenerateDashboard();
      return;
    }

    if (currentModified > lastModified) {
      lastModified = currentModified;
      // Debounce rapid changes
      if (watchTimeout) {
        clearTimeout(watchTimeout);
      }
      watchTimeout = setTimeout(() => {
        regenerateDashboard();
      }, 500);
    }
  } catch (error) {
    console.error(`Error checking file: ${error.message}`);
  }
}

function startWatching() {
  console.log(`🛡️  Watching ${sourceOfTruthPath} for changes...`);
  console.log('📊 Eternal dashboard will auto-regenerate on changes');
  console.log('💡 Open DRIFT_DASHBOARD_ETERNAL.md in Cursor and use preview pane');
  console.log('🔄 Press Ctrl+C to stop\n');

  // Initial check
  checkFile();

  // Watch file for changes
  fs.watchFile(sourceOfTruthPath, { interval: 1000 }, (curr, prev) => {
    if (curr.mtime.getTime() !== prev.mtime.getTime()) {
      checkFile();
    }
  });

  // Also poll every 2 seconds as backup
  setInterval(checkFile, 2000);
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛡️  Stopping watcher...');
  fs.unwatchFile(sourceOfTruthPath);
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n🛡️  Stopping watcher...');
  fs.unwatchFile(sourceOfTruthPath);
  process.exit(0);
});

// Start watching
startWatching();

