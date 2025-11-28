#!/usr/bin/env node
/**
 * BOUNDARY WATCHER (Native - No Dependencies)
 * 
 * Watches for file changes using Node's built-in fs.watch
 * Automatically updates source of truth and generates dashboards
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const workspaceRoot = path.resolve(__dirname, '..');

// Debounce function to avoid excessive updates
let updateTimeout = null;
const DEBOUNCE_MS = 1000; // Wait 1 second after last change

function shouldIgnore(filePath) {
  const ignorePatterns = [
    'node_modules',
    '.git',
    '.md',
    '.ai-context-source-of-truth.json',
    '__pycache__',
    '.DS_Store',
    'dist',
    'build',
    '.log'
  ];
  
  return ignorePatterns.some(pattern => filePath.includes(pattern));
}

function updateSourceAndDashboards() {
  if (updateTimeout) {
    clearTimeout(updateTimeout);
  }
  
  updateTimeout = setTimeout(() => {
    try {
      console.log('[Boundary Change] Updating source of truth...');
      execSync('node scripts/update-source-of-truth.js', {
        cwd: workspaceRoot,
        stdio: 'inherit'
      });
      
      console.log('[Boundary Change] Generating dashboards...');
      execSync('node scripts/generate-dashboards.js', {
        cwd: workspaceRoot,
        stdio: 'inherit'
      });
      
      console.log('[Boundary Change] Update complete\n');
    } catch (error) {
      console.error('Error updating source of truth:', error.message);
    }
  }, DEBOUNCE_MS);
}

function watchDirectory(dir) {
  try {
    const watcher = fs.watch(dir, { recursive: true }, (eventType, filename) => {
      if (!filename || shouldIgnore(filename)) {
        return;
      }
      
      const fullPath = path.join(dir, filename);
      console.log(`[Boundary Change] ${eventType}: ${filename}`);
      updateSourceAndDashboards();
    });
    
    watcher.on('error', (error) => {
      console.error('Watcher error:', error.message);
    });
    
    return watcher;
  } catch (error) {
    // Directory might not exist or might not support recursive watching
    return null;
  }
}

// Start watching
console.log('Boundary Watcher Active (Native)');
console.log('Watching for changes in:', workspaceRoot);
console.log('Press Ctrl+C to stop\n');

const watcher = watchDirectory(workspaceRoot);

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\nBoundary Watcher Stopped');
  if (watcher) {
    watcher.close();
  }
  process.exit(0);
});

