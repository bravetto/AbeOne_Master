#!/usr/bin/env node
/**
 * READ AI CONTEXT SOURCE OF TRUTH
 * 
 * Reads and displays AI-optimized context source of truth
 * Optimized for AI consumption across context windows
 * Provides cross-context clarity
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
 */

const fs = require('fs');
const path = require('path');

const workspaceRoot = path.resolve(__dirname, '..');
const sourceOfTruthPath = path.join(workspaceRoot, '.ai-context-source-of-truth.json');

function readAIContext() {
  if (!fs.existsSync(sourceOfTruthPath)) {
    console.log(JSON.stringify({
      error: "Source of truth not found",
      message: "Run update-ai-context-source-of-truth.js first"
    }, null, 2));
    return null;
  }
  
  try {
    const sourceOfTruth = JSON.parse(fs.readFileSync(sourceOfTruthPath, 'utf8'));
    return sourceOfTruth;
  } catch (err) {
    console.log(JSON.stringify({
      error: "Failed to read source of truth",
      message: err.message
    }, null, 2));
    return null;
  }
}

// Output for AI consumption
if (require.main === module) {
  const context = readAIContext();
  if (context) {
    // Output full context (AI-optimized JSON)
    console.log(JSON.stringify(context, null, 2));
  }
}

module.exports = { readAIContext };

