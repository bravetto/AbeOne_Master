#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const lockfilePath = path.join(__dirname, '..', '.ignore-pattern-lock.json');
const computeScript = path.join(__dirname, 'compute-ignore-lock.js');
const verifyScript = path.join(__dirname, 'verify-ignore-lock.js');

console.log('🔒 Generating ignore-pattern lockfile...');

// Generate lockfile
const output = execSync(`node ${computeScript}`, { encoding: 'utf8' });
fs.writeFileSync(lockfilePath, output, 'utf8');

console.log('✅ Lockfile generated');

// Verify lockfile
console.log('🔍 Verifying lockfile...');
try {
  execSync(`node ${verifyScript}`, { stdio: 'inherit' });
  console.log('✅ Lockfile verified - SEALED');
} catch (error) {
  console.error('❌ Lockfile verification failed');
  process.exit(1);
}

