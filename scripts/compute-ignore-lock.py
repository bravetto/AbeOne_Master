#!/usr/bin/env python3
import json
import hashlib
from datetime import datetime

# Arrays must match compute-ignore-lock.js
GLOBAL_IGNORES = [
    'node_modules',
    '.git',
    'dist',
    'build',
    '.next',
    'out',
    '.vscode',
    '.idea',
    '__pycache__',
    '.DS_Store',
    'Thumbs.db'
]

GLOBAL_IGNORES_CHOKIDAR = [
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
]

# SUBSTRATE-REQUIRED: Validate arrays before hashing
if not GLOBAL_IGNORES:
    raise ValueError("SUBSTRATE-REQUIRED: GLOBAL_IGNORES array is empty")
if not GLOBAL_IGNORES_CHOKIDAR:
    raise ValueError("SUBSTRATE-REQUIRED: GLOBAL_IGNORES_CHOKIDAR array is empty")

# Compute hashes from actual substrate (UTF-8 normalized)
hash1 = hashlib.sha256(json.dumps(GLOBAL_IGNORES, separators=(',', ':'), sort_keys=False).encode()).hexdigest()
hash2 = hashlib.sha256(json.dumps(GLOBAL_IGNORES_CHOKIDAR, separators=(',', ':'), sort_keys=False).encode()).hexdigest()
build_id = hashlib.sha256((hash1 + hash2).encode()).hexdigest()[:16]
timestamp = datetime.utcnow().isoformat() + 'Z'

lockfile = {
    'GLOBAL_IGNORES': {
        'items': GLOBAL_IGNORES,
        'digest': hash1
    },
    'GLOBAL_IGNORES_CHOKIDAR': {
        'items': GLOBAL_IGNORES_CHOKIDAR,
        'digest': hash2
    },
    'build_id': build_id,
    'timestamp': timestamp,
    'ignore_system_state': 'SEALED'
}

import os
lockfile_path = os.path.join(os.path.dirname(__file__), '..', '.ignore-pattern-lock.json')
with open(lockfile_path, 'w') as f:
    json.dump(lockfile, f, indent=2)
print(' Lockfile generated and SEALED')
print(f'   Digest GLOBAL_IGNORES: {hash1}')
print(f'   Digest GLOBAL_IGNORES_CHOKIDAR: {hash2}')
print(f'   Build ID: {build_id}')
print(f'   Timestamp: {timestamp}')

