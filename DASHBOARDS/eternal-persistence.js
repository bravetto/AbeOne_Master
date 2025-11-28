#!/usr/bin/env node
/**
 * ETERNAL PERSISTENCE SYSTEM
 * 
 * Ensures dashboards are never lost or erased
 * Git tracking, backups, version control
 * Eternal solution for dashboard persistence
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + ALRAX
 */

const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');

const workspaceRoot = path.resolve(__dirname, '..');
const dashboardsDir = __dirname;
const backupsDir = path.join(dashboardsDir, '.backups');
const gitignorePath = path.join(dashboardsDir, '.gitignore');

// Ensure backups directory exists
if (!fs.existsSync(backupsDir)) {
  fs.mkdirSync(backupsDir, { recursive: true });
}

function ensureGitTracking() {
  // Ensure .gitignore doesn't exclude dashboards
  let gitignore = '';
  if (fs.existsSync(gitignorePath)) {
    gitignore = fs.readFileSync(gitignorePath, 'utf8');
  }
  
  // Remove any exclusions for dashboards
  const lines = gitignore.split('\n').filter(line => {
    return !line.includes('DASHBOARDS/') && 
           !line.includes('*.html') &&
           !line.includes('.backups/');
  });
  
  // Add explicit includes
  lines.push('# Dashboard files are tracked');
  lines.push('!DASHBOARDS/**/*.html');
  lines.push('!DASHBOARDS/**/*.md');
  lines.push('!DASHBOARDS/**/*.json');
  lines.push('!DASHBOARDS/**/*.js');
  lines.push('# But not backup files');
  lines.push('.backups/');
  
  fs.writeFileSync(gitignorePath, lines.join('\n'), 'utf8');
  
  // Add all dashboard files to git
  try {
    execSync('git add DASHBOARDS/', { 
      cwd: workspaceRoot, 
      stdio: 'ignore' 
    });
    console.log(' Dashboard files tracked in git');
  } catch (error) {
    // Not a git repo or git not available
    console.log('ℹ  Git tracking skipped (not in git repo)');
  }
}

function createBackup(filePath) {
  if (!fs.existsSync(filePath)) return null;
  
  const fileName = path.basename(filePath);
  const timestamp = Date.now();
  const backupPath = path.join(backupsDir, `${fileName}.${timestamp}.backup`);
  
  fs.copyFileSync(filePath, backupPath);
  return backupPath;
}

function backupAllDashboards() {
  console.log(' Creating backups of all dashboards...');
  
  const registryPath = path.join(dashboardsDir, 'DASHBOARD_REGISTRY.json');
  if (!fs.existsSync(registryPath)) {
    console.error(' Dashboard registry not found');
    return;
  }
  
  const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
  let backedUp = 0;
  
  Object.values(registry.dashboards).forEach(category => {
    category.forEach(dashboard => {
      if (dashboard.file) {
        const filePath = path.join(dashboardsDir, dashboard.file);
        if (fs.existsSync(filePath)) {
          const backup = createBackup(filePath);
          if (backup) {
            backedUp++;
            console.log(`    Backed up: ${dashboard.name}`);
          }
        }
      }
    });
  });
  
  console.log(`\n Backed up ${backedUp} dashboard files\n`);
}

function setupAutoBackup() {
  console.log(' Setting up auto-backup...');
  
  // Create backup script
  const backupScript = `#!/bin/bash
# Auto-backup script for dashboards
cd "${dashboardsDir}"
node eternal-persistence.js --backup
`;
  
  const backupScriptPath = path.join(dashboardsDir, 'auto-backup.sh');
  fs.writeFileSync(backupScriptPath, backupScript, 'utf8');
  fs.chmodSync(backupScriptPath, '755');
  
  console.log(' Auto-backup script created');
  console.log(' Run: node eternal-persistence.js --backup');
}

function restoreFromBackup(fileName, timestamp = null) {
  const backups = fs.readdirSync(backupsDir)
    .filter(f => f.startsWith(fileName) && f.endsWith('.backup'))
    .sort()
    .reverse();
  
  if (backups.length === 0) {
    console.error(` No backups found for ${fileName}`);
    return false;
  }
  
  const backupFile = timestamp 
    ? backups.find(b => b.includes(timestamp))
    : backups[0]; // Most recent
  
  if (!backupFile) {
    console.error(` Backup not found`);
    return false;
  }
  
  const backupPath = path.join(backupsDir, backupFile);
  const targetPath = path.join(dashboardsDir, fileName);
  
  fs.copyFileSync(backupPath, targetPath);
  console.log(` Restored ${fileName} from backup`);
  return true;
}

function listBackups() {
  const backups = fs.readdirSync(backupsDir)
    .filter(f => f.endsWith('.backup'))
    .sort()
    .reverse();
  
  if (backups.length === 0) {
    console.log('No backups found');
    return;
  }
  
  console.log('\n AVAILABLE BACKUPS\n');
  backups.forEach(backup => {
    const stats = fs.statSync(path.join(backupsDir, backup));
    const date = new Date(stats.mtime).toLocaleString();
    console.log(`   ${backup} (${date})`);
  });
  console.log('');
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case '--setup':
  case 'setup':
    ensureGitTracking();
    setupAutoBackup();
    console.log('\n Eternal persistence setup complete!\n');
    break;
    
  case '--backup':
  case 'backup':
    backupAllDashboards();
    break;
    
  case '--restore':
  case 'restore':
    const fileName = args[1];
    const timestamp = args[2];
    if (!fileName) {
      console.error(' File name required');
      process.exit(1);
    }
    restoreFromBackup(fileName, timestamp);
    break;
    
  case '--list':
  case 'list':
    listBackups();
    break;
    
  default:
    console.log(`
  ETERNAL PERSISTENCE SYSTEM

Usage:
  node eternal-persistence.js setup      # Setup git tracking and auto-backup
  node eternal-persistence.js backup     # Create backups of all dashboards
  node eternal-persistence.js restore <file> [timestamp]  # Restore from backup
  node eternal-persistence.js list       # List available backups

Examples:
  node eternal-persistence.js setup
  node eternal-persistence.js backup
  node eternal-persistence.js restore drift-dashboard-eternal.html
  node eternal-persistence.js list
`);
}

