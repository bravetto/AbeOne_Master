#!/usr/bin/env node
/**
 * CHECK GIT STATUS
 * 
 * Gets current git commit hash and status
 * Returns git information
 */

const { execSync } = require('child_process');
const path = require('path');

function commitHash() {
  try {
    const workspaceRoot = path.join(__dirname, '..', '..');
    const hash = execSync('git rev-parse --short HEAD 2>/dev/null || echo "unknown"', {
      cwd: workspaceRoot,
      encoding: 'utf8'
    });
    return hash.trim();
  } catch (error) {
    return 'unknown';
  }
}

function checkGit() {
  return {
    commit: commitHash(),
    status: 'ok' // Can be expanded to check for uncommitted changes, etc.
  };
}

// Export both for flexibility
checkGit.commitHash = commitHash;
module.exports = checkGit;

