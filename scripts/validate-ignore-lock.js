#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const GLOBAL_IGNORES = [
  'node_modules', '.git', 'dist', 'build', '.next', 'out',
  '.vscode', '.idea', '__pycache__', '.DS_Store', 'Thumbs.db'
];

const GLOBAL_IGNORES_CHOKIDAR = [
  '**/node_modules', '**/.git', '**/dist', '**/build', '**/.next', '**/out',
  '**/.vscode', '**/.idea', '**/__pycache__', '**/.DS_Store', '**/Thumbs.db',
  '**/*.log', '.ai-context-source-of-truth.json'
];

const lockFilePath = path.join(__dirname, '..', '.ignore-pattern-lock.json');

function validateHashNotFake(hash) {
  if (!hash || hash.length !== 64 || !/^[0-9a-f]{64}$/i.test(hash)) return false;
  return !/(.)\1{5,}/.test(hash); // No repeating patterns
}

function validateIgnoreLock() {
  if (!fs.existsSync(lockFilePath)) {
    console.error(' .ignore-pattern-lock.json not found');
    console.error('   Run: node scripts/compute-ignore-lock.js > .ignore-pattern-lock.json');
    process.exit(1);
  }

  let lockFile;
  try {
    lockFile = JSON.parse(fs.readFileSync(lockFilePath, 'utf8'));
  } catch (err) {
    console.error(` Invalid JSON: ${err.message}`);
    process.exit(1);
  }

  if (!lockFile.GLOBAL_IGNORES || !lockFile.GLOBAL_IGNORES_CHOKIDAR) {
    console.error(' Lock file missing required sections');
    process.exit(1);
  }

  const expectedHash1 = crypto.createHash('sha256').update(JSON.stringify(GLOBAL_IGNORES)).digest('hex');
  const expectedHash2 = crypto.createHash('sha256').update(JSON.stringify(GLOBAL_IGNORES_CHOKIDAR)).digest('hex');
  const storedHash1 = lockFile.GLOBAL_IGNORES.digest;
  const storedHash2 = lockFile.GLOBAL_IGNORES_CHOKIDAR.digest;

  const arraysMatch = 
    JSON.stringify(lockFile.GLOBAL_IGNORES.items) === JSON.stringify(GLOBAL_IGNORES) &&
    JSON.stringify(lockFile.GLOBAL_IGNORES_CHOKIDAR.items) === JSON.stringify(GLOBAL_IGNORES_CHOKIDAR);

  if (!arraysMatch) {
    console.error(' Lock file arrays don\'t match expected values');
    process.exit(1);
  }

  if (storedHash1 !== expectedHash1 || storedHash2 !== expectedHash2) {
    console.error(' Lock file hashes don\'t match computed values');
    process.exit(1);
  }

  if (!validateHashNotFake(storedHash1) || !validateHashNotFake(storedHash2)) {
    console.error(' Lock file contains fake hash patterns');
    process.exit(1);
  }

  console.log(' Lock file validated');
  return 0;
}

// Run if called directly
if (require.main === module) {
  const exitCode = validateIgnoreLock();
  process.exit(exitCode);
}

module.exports = { validateIgnoreLock };
