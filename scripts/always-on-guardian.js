#!/usr/bin/env node
/**
 * ALWAYS-ON GUARDIAN
 * 
 * Ultra-lightweight check that runs on every interaction
 * Returns JSON for easy integration
 * Non-blocking, informative, helpful
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + Abë (530 Hz)
 */

const fs = require('fs');
const path = require('path');

function quickCheck() {
  const currentDir = process.cwd();
  let workspaceRoot = currentDir;
  
  // Find workspace root
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(workspaceRoot, 'PROJECT_MASTER_INDEX.md'))) {
      break;
    }
    const parent = path.dirname(workspaceRoot);
    if (parent === workspaceRoot) break;
    workspaceRoot = parent;
  }

  const result = {
    currentDir: path.basename(currentDir),
    project: null,
    status: 'unknown',
    tips: []
  };

  // Quick check for project boundary
  const boundaryPath = path.join(currentDir, '.project-boundary');
  if (fs.existsSync(boundaryPath)) {
    try {
      const boundary = JSON.parse(fs.readFileSync(boundaryPath, 'utf8'));
      result.project = boundary.projectName || path.basename(currentDir);
      result.status = boundary.status || 'unknown';
      result.version = boundary.version || 'unknown';
      
      if (boundary.status === 'ACTIVE') {
        result.message = ` Working in ${result.project} - active project!`;
        result.emoji = '';
      } else if (boundary.status === 'LEGACY') {
        result.message = ` In legacy directory. Active: ${boundary.activeDirectory || 'check PROJECT_STATUS.md'}`;
        result.emoji = '';
        result.tips.push(`Consider switching to: ${boundary.activeDirectory || 'active directory'}`);
      }
    } catch (err) {
      // Silent fail
    }
  }

  // Check PROJECT_STATUS.md as fallback
  const statusPath = path.join(currentDir, 'PROJECT_STATUS.md');
  if (fs.existsSync(statusPath) && !result.project) {
    const content = fs.readFileSync(statusPath, 'utf8');
    const nameMatch = content.match(/\*\*Project Name\*\*: (.+)/);
    const statusMatch = content.match(/\*\*Status\*\*: (.+)/);
    
    if (nameMatch) result.project = nameMatch[1].trim();
    if (statusMatch) {
      const status = statusMatch[1].trim();
      if (status.includes('ACTIVE')) result.status = 'ACTIVE';
      else if (status.includes('LEGACY')) result.status = 'LEGACY';
    }
  }

  // Add helpful tips
  if (result.status === 'ACTIVE') {
    result.tips.push(' Run validation scripts anytime: node scripts/validate-project-boundaries.js');
    result.tips.push(' Check PROJECT_STATUS.md for project details');
  }

  return result;
}

// Output JSON for easy parsing
if (require.main === module) {
  const result = quickCheck();
  console.log(JSON.stringify(result, null, 2));
}

module.exports = { quickCheck };

