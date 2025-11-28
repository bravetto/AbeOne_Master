#!/usr/bin/env node
/**
 * UPDATE DRIFT STATUS FILE
 * 
 * Updates .drift-status.txt with current drift guardian status
 * Can be watched/auto-refreshed for always-visible status
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + Abë (530 Hz)
 */

const fs = require('fs');
const path = require('path');
const GentleDriftGuardian = require('./gentle-drift-guardian');

const workspaceRoot = path.resolve(__dirname, '..');
const statusFile = path.join(workspaceRoot, '.drift-status.txt');
const jsonFile = path.join(workspaceRoot, '.drift-status.json');

// Update status
const guardian = new GentleDriftGuardian();
const output = guardian.formatOutput();
const jsonData = guardian.check();

// Write text status
fs.writeFileSync(statusFile, output, 'utf8');

// Write JSON status
fs.writeFileSync(jsonFile, JSON.stringify({
  ...jsonData,
  timestamp: new Date().toISOString(),
  updated: new Date().toLocaleTimeString()
}, null, 2), 'utf8');

console.log('✅ Drift status updated');

