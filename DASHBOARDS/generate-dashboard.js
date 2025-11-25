#!/usr/bin/env node
/**
 * ONE-CLICK DASHBOARD GENERATOR
 * 
 * Simple click/command to generate any dashboard
 * Reads from DASHBOARD_REGISTRY.json
 * Ensures eternal persistence
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + ALRAX
 * EEAaO: Everything Everywhere All At Once
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const workspaceRoot = path.resolve(__dirname, '..');
const registryPath = path.join(__dirname, 'DASHBOARD_REGISTRY.json');
const backupsDir = path.join(__dirname, '.backups');

// Ensure backups directory exists
if (!fs.existsSync(backupsDir)) {
  fs.mkdirSync(backupsDir, { recursive: true });
}

function loadRegistry() {
  if (!fs.existsSync(registryPath)) {
    console.error(' Dashboard registry not found!');
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(registryPath, 'utf8'));
}

function backupDashboard(dashboardPath) {
  if (!fs.existsSync(dashboardPath)) return;
  
  const backupPath = path.join(backupsDir, path.basename(dashboardPath) + '.' + Date.now());
  fs.copyFileSync(dashboardPath, backupPath);
  return backupPath;
}

function generateDashboard(dashboardId, registry) {
  const dashboard = findDashboard(dashboardId, registry);
  if (!dashboard) {
    console.error(` Dashboard "${dashboardId}" not found in registry`);
    return false;
  }

  console.log(`  Generating dashboard: ${dashboard.name}`);

  // Backup existing if exists
  const dashboardPath = path.join(__dirname, dashboard.file);
  if (fs.existsSync(dashboardPath)) {
    const backup = backupDashboard(dashboardPath);
    console.log(`    Backed up to: ${backup}`);
  }

  // Generate based on type
  switch (dashboard.type) {
    case 'eternal':
      return generateEternalDashboard(dashboard, registry);
    case 'monitoring':
      return generateMonitoringDashboard(dashboard, registry);
    case 'product':
      return generateProductDashboard(dashboard, registry);
    default:
      console.error(` Unknown dashboard type: ${dashboard.type}`);
      return false;
  }
}

function findDashboard(id, registry) {
  for (const category of Object.values(registry.dashboards)) {
    const dashboard = category.find(d => d.id === id);
    if (dashboard) return dashboard;
  }
  return null;
}

function generateEternalDashboard(dashboard, registry) {
  // Use existing eternal dashboard generator
  const generatorPath = path.join(workspaceRoot, 'scripts', 'generate-eternal-dashboard.js');
  if (fs.existsSync(generatorPath)) {
    const child = spawn('node', [generatorPath], {
      cwd: workspaceRoot,
      stdio: 'inherit'
    });
    child.on('close', (code) => {
      if (code === 0) {
        console.log(` Generated: ${dashboard.name}`);
        ensureGitTracking(dashboard.file);
      }
    });
    return true;
  }
  return false;
}

function generateMonitoringDashboard(dashboard, registry) {
  // Copy from root if exists, or generate new
  const sourcePath = path.join(workspaceRoot, path.basename(dashboard.file));
  const targetPath = path.join(__dirname, dashboard.file);
  
  if (fs.existsSync(sourcePath)) {
    // Ensure directory exists
    const targetDir = path.dirname(targetPath);
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }
    fs.copyFileSync(sourcePath, targetPath);
    console.log(` Copied: ${dashboard.name}`);
    ensureGitTracking(dashboard.file);
    return true;
  }
  return false;
}

function generateProductDashboard(dashboard, registry) {
  if (dashboard.source) {
    const sourcePath = path.join(workspaceRoot, dashboard.source);
    const targetPath = path.join(__dirname, dashboard.file);
    
    if (fs.existsSync(sourcePath)) {
      const targetDir = path.dirname(targetPath);
      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
      }
      fs.copyFileSync(sourcePath, targetPath);
      console.log(` Copied: ${dashboard.name}`);
      ensureGitTracking(dashboard.file);
      return true;
    }
  }
  return false;
}

function ensureGitTracking(filePath) {
  const fullPath = path.join(__dirname, filePath);
  const gitPath = path.join(__dirname, '.gitignore');
  
  // Ensure .gitignore doesn't exclude dashboards
  let gitignore = '';
  if (fs.existsSync(gitPath)) {
    gitignore = fs.readFileSync(gitPath, 'utf8');
  }
  
  // Add dashboard to git if not ignored
  if (!gitignore.includes('DASHBOARDS/') && !gitignore.includes('*.html')) {
    // Run git add (non-blocking)
    const child = spawn('git', ['add', fullPath], {
      cwd: workspaceRoot,
      stdio: 'ignore'
    });
    child.unref();
  }
}

function generateAllRequired(registry) {
  const required = registry.required['human-ai-excellence'] || [];
  console.log(`  Generating all required dashboards for Human-AI Excellence...\n`);
  
  let success = 0;
  let failed = 0;
  
  required.forEach(id => {
    if (generateDashboard(id, registry)) {
      success++;
    } else {
      failed++;
    }
  });
  
  console.log(`\n Generated: ${success}`);
  if (failed > 0) {
    console.log(` Failed: ${failed}`);
  }
}

// Main
const args = process.argv.slice(2);
const registry = loadRegistry();

if (args.length === 0 || args[0] === '--all' || args[0] === 'all') {
  generateAllRequired(registry);
} else {
  const dashboardId = args[0];
  generateDashboard(dashboardId, registry);
}

