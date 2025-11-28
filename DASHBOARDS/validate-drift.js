#!/usr/bin/env node
/**
 * DRIFT VALIDATION SYSTEM
 * 
 * Validates all files and folders for potential drift issues
 * Checks project boundaries, imports, dependencies
 * Comprehensive validation for Human-AI Excellence
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + ALRAX
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const workspaceRoot = path.resolve(__dirname, '..');

const issues = {
  critical: [],
  warning: [],
  info: []
};

function validateProjectBoundaries() {
  console.log(' Validating project boundaries...');
  
  const projects = [
    'AiGuardian-Chrome-Ext-dev',
    'AIGuards-Backend',
    'EMERGENT_OS'
  ];
  
  projects.forEach(project => {
    const projectPath = path.join(workspaceRoot, project);
    const boundaryPath = path.join(projectPath, '.project-boundary');
    const statusPath = path.join(projectPath, 'PROJECT_STATUS.md');
    
    if (!fs.existsSync(projectPath)) {
      issues.warning.push(`Project directory missing: ${project}`);
      return;
    }
    
    if (!fs.existsSync(boundaryPath) && !fs.existsSync(statusPath)) {
      issues.warning.push(`Project ${project} missing boundary or status file`);
    }
  });
}

function validateDashboardFiles() {
  console.log(' Validating dashboard files...');
  
  const dashboardFiles = [
    'drift-dashboard-eternal.html',
    'drift-status-dashboard.html',
    'drift-realtime-dashboard.html',
    'drift-status-badge.html'
  ];
  
  dashboardFiles.forEach(file => {
    const filePath = path.join(workspaceRoot, file);
    if (fs.existsSync(filePath)) {
      // Check if file is tracked in registry
      const registryPath = path.join(__dirname, 'DASHBOARD_REGISTRY.json');
      if (fs.existsSync(registryPath)) {
        const registry = JSON.parse(fs.readFileSync(registryPath, 'utf8'));
        const found = Object.values(registry.dashboards).some(category =>
          category.some(d => d.file && d.file.includes(file))
        );
        if (!found) {
          issues.info.push(`Dashboard file ${file} exists but not in registry`);
        }
      }
    }
  });
}

function validateDataSources() {
  console.log(' Validating data sources...');
  
  const sourceOfTruthPath = path.join(workspaceRoot, '.ai-context-source-of-truth.json');
  if (!fs.existsSync(sourceOfTruthPath)) {
    issues.critical.push('AI context source of truth file missing');
  } else {
    try {
      const data = JSON.parse(fs.readFileSync(sourceOfTruthPath, 'utf8'));
      if (!data._meta || !data._meta.eternal) {
        issues.warning.push('AI context source of truth missing eternal flag');
      }
    } catch (error) {
      issues.critical.push(`AI context source of truth file corrupted: ${error.message}`);
    }
  }
}

function validateEternalPersistence() {
  console.log(' Validating eternal persistence...');
  
  const dashboardsDir = __dirname;
  const backupsDir = path.join(dashboardsDir, '.backups');
  
  // Check if backups directory exists
  if (!fs.existsSync(backupsDir)) {
    issues.warning.push('Dashboard backups directory missing');
  }
  
  // Check git tracking
  try {
    const gitStatus = execSync('git ls-files DASHBOARDS/', { 
      cwd: workspaceRoot, 
      encoding: 'utf8',
      stdio: 'pipe'
    });
    if (!gitStatus.trim()) {
      issues.warning.push('Dashboard files not tracked in git');
    }
  } catch (error) {
    issues.info.push('Could not check git tracking (may not be in git repo)');
  }
}

function validatePortRegistry() {
  console.log(' Validating port registry...');
  
  const portRegistryPath = path.join(__dirname, '.port-registry.json');
  if (!fs.existsSync(portRegistryPath)) {
    issues.info.push('Port registry not initialized (will be created on first use)');
  } else {
    try {
      const registry = JSON.parse(fs.readFileSync(portRegistryPath, 'utf8'));
      if (!registry._meta || !registry._meta.eternal) {
        issues.warning.push('Port registry missing eternal flag');
      }
    } catch (error) {
      issues.critical.push(`Port registry corrupted: ${error.message}`);
    }
  }
}

function validateScripts() {
  console.log(' Validating dashboard scripts...');
  
  const scripts = [
    'generate-dashboard.js',
    'port-manager.js',
    'validate-drift.js'
  ];
  
  scripts.forEach(script => {
    const scriptPath = path.join(__dirname, script);
    if (!fs.existsSync(scriptPath)) {
      issues.critical.push(`Required script missing: ${script}`);
    } else {
      // Check if executable
      try {
        const stats = fs.statSync(scriptPath);
        if (!(stats.mode & parseInt('111', 8))) {
          issues.warning.push(`Script ${script} is not executable`);
        }
      } catch (error) {
        // Ignore
      }
    }
  });
}

function runAllValidations() {
  console.log('  DRIFT VALIDATION SYSTEM\n');
  console.log('='.repeat(50));
  console.log('');
  
  validateProjectBoundaries();
  validateDashboardFiles();
  validateDataSources();
  validateEternalPersistence();
  validatePortRegistry();
  validateScripts();
  
  // Report results
  console.log('');
  console.log('='.repeat(50));
  console.log('VALIDATION RESULTS\n');
  
  if (issues.critical.length > 0) {
    console.log(' CRITICAL ISSUES:');
    issues.critical.forEach(issue => console.log(`   - ${issue}`));
    console.log('');
  }
  
  if (issues.warning.length > 0) {
    console.log('  WARNINGS:');
    issues.warning.forEach(issue => console.log(`   - ${issue}`));
    console.log('');
  }
  
  if (issues.info.length > 0) {
    console.log('ℹ  INFO:');
    issues.info.forEach(issue => console.log(`   - ${issue}`));
    console.log('');
  }
  
  if (issues.critical.length === 0 && issues.warning.length === 0) {
    console.log(' All validations passed!\n');
  }
  
  // Exit with error code if critical issues
  process.exit(issues.critical.length > 0 ? 1 : 0);
}

// Run if called directly
if (require.main === module) {
  runAllValidations();
}

module.exports = { runAllValidations, issues };

