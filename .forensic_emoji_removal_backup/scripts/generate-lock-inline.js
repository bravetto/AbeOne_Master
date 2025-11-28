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

const hash1 = crypto.createHash('sha256').update(JSON.stringify(GLOBAL_IGNORES)).digest('hex');
const hash2 = crypto.createHash('sha256').update(JSON.stringify(GLOBAL_IGNORES_CHOKIDAR)).digest('hex');
const buildId = crypto.createHash('sha256').update(hash1 + hash2).digest('hex').substring(0, 16);

const lockfile = {
  GLOBAL_IGNORES: { items: GLOBAL_IGNORES, digest: hash1 },
  GLOBAL_IGNORES_CHOKIDAR: { items: GLOBAL_IGNORES_CHOKIDAR, digest: hash2 },
  build_id: buildId,
  timestamp: new Date().toISOString(),
  ignore_system_state: 'SEALED'
};

fs.writeFileSync(path.join(__dirname, '..', '.ignore-pattern-lock.json'), JSON.stringify(lockfile, null, 2), 'utf8');
console.log('✅ Lockfile generated and SEALED');

