#!/usr/bin/env node
/**
 * BOUNDARY WATCHER
 * 
 * Watches for file changes and automatically updates source of truth
 * and generates dashboards
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 */

const chokidar = require('chokidar');
const { execSync } = require('child_process');
const path = require('path');

const workspaceRoot = path.resolve(__dirname, '..');

// GLOBAL_IGNORES: Unified ignore pattern (chokidar glob variants)
const GLOBAL_IGNORES_CHOKIDAR = [
  '**/node_modules',
  '**/.git',
  '**/dist',
  '**/build',
  '**/.next',
  '**/out',
  '**/.vscode',
  '**/.idea',
  '**/__pycache__',
  '**/.DS_Store',
  '**/Thumbs.db',
  '**/*.log',
  '.ai-context-source-of-truth.json'
];

// Watch for changes, ignoring common directories and generated files
chokidar.watch('.', {
  ignored: GLOBAL_IGNORES_CHOKIDAR,
  persistent: true,
  cwd: workspaceRoot,
  ignoreInitial: true
}).on('all', (event, filePath) => {
  console.log(`[Boundary Change] ${event}: ${filePath}`);
  
  try {
    execSync('node scripts/update-source-of-truth.js', {
      cwd: workspaceRoot,
      stdio: 'inherit'
    });
    
    execSync('node scripts/generate-dashboards.js', {
      cwd: workspaceRoot,
      stdio: 'inherit'
    });
  } catch (error) {
    console.error('Error updating source of truth:', error.message);
  }
});

console.log('Boundary Watcher Active');
console.log('Watching for changes in:', workspaceRoot);
console.log('Press Ctrl+C to stop\n');

