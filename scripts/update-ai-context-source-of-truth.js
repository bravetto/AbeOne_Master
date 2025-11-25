#!/usr/bin/env node
/**
 * UPDATE AI CONTEXT SOURCE OF TRUTH
 * 
 * Updates .ai-context-source-of-truth.json with current context
 * Optimized for AI consumption across context windows
 * Tracks multiple projects simultaneously
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
 */

const fs = require('fs');
const path = require('path');
const { quickCheck } = require('./always-on-guardian');

const workspaceRoot = path.resolve(__dirname, '..');
const sourceOfTruthPath = path.join(workspaceRoot, '.ai-context-source-of-truth.json');

function updateSourceOfTruth() {
  // Get current context
  const currentContext = quickCheck();
  const currentDir = process.cwd();
  const currentDirName = path.basename(currentDir);
  
  // Read existing source of truth
  let sourceOfTruth = {};
  if (fs.existsSync(sourceOfTruthPath)) {
    try {
      sourceOfTruth = JSON.parse(fs.readFileSync(sourceOfTruthPath, 'utf8'));
    } catch (err) {
      // If corrupted, start fresh
      sourceOfTruth = {};
    }
  }
  
  // Initialize structure if needed
  if (!sourceOfTruth.workspace) {
    sourceOfTruth.workspace = {
      root: path.basename(workspaceRoot),
      currentDirectory: null,
      currentProject: null,
      contextWindows: []
    };
  }
  
  if (!sourceOfTruth.contextTracking) {
    sourceOfTruth.contextTracking = {
      multiProjectAware: true,
      note: "Users work on multiple projects simultaneously across different context windows",
      activeContexts: [],
      recentContexts: []
    };
  }
  
  // Update current context
  sourceOfTruth.workspace.currentDirectory = currentDirName;
  sourceOfTruth.workspace.currentProject = currentContext.project || currentDirName;
  
  // Update timestamp
  const now = new Date();
  sourceOfTruth._meta = sourceOfTruth._meta || {};
  sourceOfTruth._meta.lastUpdated = now.toISOString();
  sourceOfTruth._meta.lastUpdatedReadable = now.toLocaleString();
  
  // Track context window (add to recent contexts)
  const contextEntry = {
    directory: currentDirName,
    project: currentContext.project || currentDirName,
    status: currentContext.status || 'unknown',
    timestamp: now.toISOString(),
    timestampReadable: now.toLocaleString()
  };
  
  // Add to recent contexts (keep last 10)
  if (!sourceOfTruth.contextTracking.recentContexts) {
    sourceOfTruth.contextTracking.recentContexts = [];
  }
  sourceOfTruth.contextTracking.recentContexts.unshift(contextEntry);
  sourceOfTruth.contextTracking.recentContexts = sourceOfTruth.contextTracking.recentContexts.slice(0, 10);
  
  // Update active contexts (current + recent unique)
  const activeContexts = [contextEntry];
  const seen = new Set([currentDirName]);
  
  for (const ctx of sourceOfTruth.contextTracking.recentContexts) {
    if (!seen.has(ctx.directory) && ctx.directory !== currentDirName) {
      activeContexts.push(ctx);
      seen.add(ctx.directory);
    }
  }
  sourceOfTruth.contextTracking.activeContexts = activeContexts.slice(0, 5);
  
  // Update project lastWorkedOn if in project directory
  if (sourceOfTruth.projects && sourceOfTruth.projects.active) {
    for (const project of sourceOfTruth.projects.active) {
      if (currentDirName === project.directory.replace('/', '') || 
          currentDir.includes(project.directory)) {
        project.lastWorkedOn = now.toISOString();
        project.lastWorkedOnReadable = now.toLocaleString();
        
        // Add to project's context windows
        if (!project.contextWindows) {
          project.contextWindows = [];
        }
        project.contextWindows.unshift({
          directory: currentDirName,
          timestamp: now.toISOString(),
          timestampReadable: now.toLocaleString()
        });
        project.contextWindows = project.contextWindows.slice(0, 5);
      }
    }
  }
  
  // Write updated source of truth
  fs.writeFileSync(
    sourceOfTruthPath,
    JSON.stringify(sourceOfTruth, null, 2),
    'utf8'
  );
  
  return sourceOfTruth;
}

// Run if called directly
if (require.main === module) {
  try {
    updateSourceOfTruth();
  } catch (err) {
    // Silent fail - don't block
    process.exit(0);
  }
}

module.exports = { updateSourceOfTruth };

