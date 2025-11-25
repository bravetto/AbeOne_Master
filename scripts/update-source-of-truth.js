#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// ---- SINGLE SOURCE OF TRUTH FILE ----
const SOURCE = path.join(__dirname, '..', '.ai-context-source-of-truth.json');

// ---- STABLE SYSTEM CHECK MODULES ----
const checkBackend = require('./modules/checkBackend');
const checkExtension = require('./modules/checkExtension');
const checkGit = require('./modules/checkGit');
const calculateHealth = require('./modules/calculateHealth');

// ---- READ OLD SOURCE ----
let old = {};
try {
  old = JSON.parse(fs.readFileSync(SOURCE, 'utf8'));
} catch (e) { 
  old = {}; 
}

// ---- GATHER SYSTEM STATUS ----
const backendStatus = checkBackend();
const extensionStatus = checkExtension();
const gitStatus = checkGit();

const status = {
  timestamp: new Date().toISOString(),
  commit: gitStatus.commit,
  backend: backendStatus,
  extension: extensionStatus,
  health: calculateHealth({
    backend: backendStatus,
    extension: extensionStatus,
    commit: gitStatus.commit
  }),
};

// ---- WRITE NEW SOURCE ----
fs.writeFileSync(SOURCE, JSON.stringify(status, null, 2));

// Echo diff
console.log('Source of Truth Updated:', status);

