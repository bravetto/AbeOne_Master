#!/usr/bin/env node
/**
 * TRIGGER VISUAL STATUS UPDATE (Node.js)
 * 
 * Lightweight Node.js trigger for DRIFT_STATUS_VISUAL.md updates
 * Also updates AI context source of truth
 * Runs silently, non-blocking, fast execution
 * Called automatically on chat interactions (input + output)
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
 */

const { spawn } = require('child_process');
const path = require('path');
const { updateSourceOfTruth } = require('./update-ai-context-source-of-truth');
const { generateEternalDashboard } = require('./generate-eternal-dashboard');

const scriptDir = __dirname;
const workspaceRoot = path.resolve(scriptDir, '..');
const updateScript = path.join(scriptDir, 'update-all-visual-status.sh');

// Update AI context source of truth (synchronous, fast)
try {
  updateSourceOfTruth();
} catch (err) {
  // Silent fail - don't block
}

// Generate eternal dashboard (synchronous, fast)
try {
  generateEternalDashboard();
} catch (err) {
  // Silent fail - don't block
}

// Spawn visual status update in background (non-blocking)
const child = spawn('bash', [updateScript], {
  cwd: workspaceRoot,
  detached: true,
  stdio: 'ignore'
});

// Unref to allow parent process to exit independently
child.unref();

// Exit immediately (non-blocking)
process.exit(0);

