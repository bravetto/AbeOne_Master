#!/usr/bin/env node
/**
 * VALIDATE AI CONTEXT SOURCE OF TRUTH
 * 
 * Validates AI-optimized source of truth for:
 * - AI pattern optimization
 * - Source pattern compliance
 * - Eternal validation
 * - Multi-project awareness
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
 */

const fs = require('path');
const path = require('path');
const { readAIContext } = require('./read-ai-context');

const workspaceRoot = path.resolve(__dirname, '..');
const sourceOfTruthPath = path.join(workspaceRoot, '.ai-context-source-of-truth.json');

function validateAIContext() {
  const results = {
    validated: true,
    errors: [],
    warnings: [],
    checks: {}
  };
  
  // Read source of truth
  const context = readAIContext();
  if (!context) {
    results.validated = false;
    results.errors.push("Source of truth file not found or unreadable");
    return results;
  }
  
  // Check 1: AI Pattern Optimization
  results.checks.aiPatternOptimization = {
    passed: true,
    details: []
  };
  
  if (!context.aiOptimization) {
    results.checks.aiPatternOptimization.passed = false;
    results.errors.push("Missing aiOptimization section");
  } else {
    const aiOpt = context.aiOptimization;
    if (aiOpt.format !== "JSON") {
      results.warnings.push("Format should be JSON for AI parsing");
    }
    if (!aiOpt.parsing || aiOpt.parsing !== "optimized") {
      results.warnings.push("Parsing optimization not marked");
    }
    if (!aiOpt.keyFields || !Array.isArray(aiOpt.keyFields)) {
      results.errors.push("Missing or invalid keyFields array");
      results.checks.aiPatternOptimization.passed = false;
    }
    if (!aiOpt.updateTriggers || !Array.isArray(aiOpt.updateTriggers)) {
      results.errors.push("Missing or invalid updateTriggers array");
      results.checks.aiPatternOptimization.passed = false;
    } else {
      if (!aiOpt.updateTriggers.includes("chat_input") || 
          !aiOpt.updateTriggers.includes("chat_output")) {
        results.errors.push("updateTriggers must include chat_input and chat_output");
        results.checks.aiPatternOptimization.passed = false;
      }
    }
  }
  
  // Check 2: Source Pattern Compliance
  results.checks.sourcePattern = {
    passed: true,
    details: []
  };
  
  if (!context._meta) {
    results.errors.push("Missing _meta section");
    results.checks.sourcePattern.passed = false;
  } else {
    if (!context._meta.eternal) {
      results.warnings.push("Eternal flag not set");
    }
    if (!context._meta.validated) {
      results.warnings.push("Validated flag not set");
    }
    if (context._meta.updateFrequency !== "2x per chat sequence (input + output)") {
      results.warnings.push("Update frequency not properly documented");
    }
  }
  
  // Check 3: Multi-Project Awareness
  results.checks.multiProjectAwareness = {
    passed: true,
    details: []
  };
  
  if (!context.contextTracking) {
    results.errors.push("Missing contextTracking section");
    results.checks.multiProjectAwareness.passed = false;
  } else {
    if (context.contextTracking.multiProjectAware !== true) {
      results.errors.push("multiProjectAware must be true");
      results.checks.multiProjectAwareness.passed = false;
    }
    if (!context.contextTracking.note || 
        !context.contextTracking.note.includes("multiple projects")) {
      results.warnings.push("Multi-project note missing or unclear");
    }
  }
  
  // Check 4: Projects Structure
  results.checks.projectsStructure = {
    passed: true,
    details: []
  };
  
  if (!context.projects) {
    results.errors.push("Missing projects section");
    results.checks.projectsStructure.passed = false;
  } else {
    if (!context.projects.active || !Array.isArray(context.projects.active)) {
      results.errors.push("Missing or invalid active projects array");
      results.checks.projectsStructure.passed = false;
    }
    if (!context.projects.legacy || !Array.isArray(context.projects.legacy)) {
      results.warnings.push("Missing legacy projects array (may be empty)");
    }
  }
  
  // Check 5: Workspace Structure
  results.checks.workspaceStructure = {
    passed: true,
    details: []
  };
  
  if (!context.workspace) {
    results.errors.push("Missing workspace section");
    results.checks.workspaceStructure.passed = false;
  } else {
    if (!context.workspace.root) {
      results.errors.push("Missing workspace.root");
      results.checks.workspaceStructure.passed = false;
    }
  }
  
  // Check 6: Validation Section
  results.checks.validationSection = {
    passed: true,
    details: []
  };
  
  if (!context.validation) {
    results.warnings.push("Missing validation section");
  } else {
    if (context.validation.sourcePattern !== true) {
      results.warnings.push("sourcePattern validation not marked true");
    }
    if (context.validation.aiPattern !== true) {
      results.warnings.push("aiPattern validation not marked true");
    }
    if (context.validation.eternal !== true) {
      results.warnings.push("eternal validation not marked true");
    }
    if (context.validation.autoUpdate !== true) {
      results.warnings.push("autoUpdate validation not marked true");
    }
  }
  
  // Final validation
  if (results.errors.length > 0) {
    results.validated = false;
  }
  
  return results;
}

// Run validation
if (require.main === module) {
  const results = validateAIContext();
  console.log(JSON.stringify(results, null, 2));
  
  if (!results.validated) {
    process.exit(1);
  }
}

module.exports = { validateAIContext };

