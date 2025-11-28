#!/usr/bin/env node
/**
 * WATCH DASHBOARD UPDATES
 * 
 * Watches .ai-context-source-of-truth.json for changes
 * Triggers visual updates when file changes
 * Ensures dashboards stay in sync with real-time data
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const workspaceRoot = path.resolve(__dirname, '..');
const sourceOfTruthPath = path.join(workspaceRoot, '.ai-context-source-of-truth.json');
const triggerScript = path.join(__dirname, 'trigger-visual-update.js');

let lastModified = null;
let watchTimeout = null;

function triggerUpdate() {
  // Trigger visual update script
  const child = spawn('node', [triggerScript], {
    cwd: workspaceRoot,
    detached: true,
    stdio: 'ignore'
  });
  child.unref();
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
      return;
    }

    if (currentModified > lastModified) {
      lastModified = currentModified;
      console.log(`[${new Date().toISOString()}] File changed, triggering update...`);
      triggerUpdate();
    }
  } catch (error) {
    console.error(`Error checking file: ${error.message}`);
  }
}

function startWatching() {
  console.log(`Watching ${sourceOfTruthPath} for changes...`);
  console.log('Press Ctrl+C to stop\n');

  // Initial check
  checkFile();

  // Watch file for changes
  fs.watchFile(sourceOfTruthPath, { interval: 1000 }, (curr, prev) => {
    if (curr.mtime.getTime() !== prev.mtime.getTime()) {
      // Debounce rapid changes
      if (watchTimeout) {
        clearTimeout(watchTimeout);
      }
      watchTimeout = setTimeout(() => {
        checkFile();
      }, 500);
    }
  });

  // Also poll every 2 seconds as backup
  setInterval(checkFile, 2000);
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\nStopping watcher...');
  fs.unwatchFile(sourceOfTruthPath);
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\nStopping watcher...');
  fs.unwatchFile(sourceOfTruthPath);
  process.exit(0);
});

// Start watching
startWatching();

