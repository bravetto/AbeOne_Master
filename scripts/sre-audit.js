#!/usr/bin/env node
/**
 * SRE AUDIT SCRIPT
 * 
 * Continuously checks for SRE compliance violations:
 * - Drift in lock file
 * - Drift in context-of-truth
 * - Hardcoded issue arrays
 * - Missing substrate checks
 * - Default masking patterns
 * - Fake hash patterns
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + SRE Enforcement
 */

const fs = require('fs');
const path = require('path');
const { validateHashNotFake } = require('./utils/substrate-validator');

const workspaceRoot = path.resolve(__dirname, '..');
const violations = [];
const warnings = [];

/**
 * Check for fake hashes in lock file
 */
function checkLockFileHashes() {
  const lockFilePath = path.join(workspaceRoot, '.ignore-pattern-lock.json');
  
  if (!fs.existsSync(lockFilePath)) {
    violations.push({
      type: 'CRITICAL',
      file: '.ignore-pattern-lock.json',
      issue: 'Lock file missing',
      fix: 'Run: node scripts/compute-ignore-lock.js > .ignore-pattern-lock.json'
    });
    return;
  }
  
  try {
    const lockData = JSON.parse(fs.readFileSync(lockFilePath, 'utf8'));
    
    if (lockData.GLOBAL_IGNORES && lockData.GLOBAL_IGNORES.digest) {
      if (!validateHashNotFake(lockData.GLOBAL_IGNORES.digest, 'GLOBAL_IGNORES.digest')) {
        violations.push({
          type: 'CRITICAL',
          file: '.ignore-pattern-lock.json',
          issue: 'Fake hash detected in GLOBAL_IGNORES.digest',
          fix: 'Regenerate lock file with real substrate hashes'
        });
      }
    }
    
    if (lockData.GLOBAL_IGNORES_CHOKIDAR && lockData.GLOBAL_IGNORES_CHOKIDAR.digest) {
      if (!validateHashNotFake(lockData.GLOBAL_IGNORES_CHOKIDAR.digest, 'GLOBAL_IGNORES_CHOKIDAR.digest')) {
        violations.push({
          type: 'CRITICAL',
          file: '.ignore-pattern-lock.json',
          issue: 'Fake hash detected in GLOBAL_IGNORES_CHOKIDAR.digest',
          fix: 'Regenerate lock file with real substrate hashes'
        });
      }
    }
  } catch (err) {
    violations.push({
      type: 'HIGH',
      file: '.ignore-pattern-lock.json',
      issue: `Failed to parse lock file: ${err.message}`,
      fix: 'Regenerate lock file'
    });
  }
}

/**
 * Check for hardcoded issue arrays
 */
function checkHardcodedIssues() {
  const checkExtensionPath = path.join(workspaceRoot, 'scripts', 'modules', 'checkExtension.js');
  
  if (!fs.existsSync(checkExtensionPath)) {
    return;
  }
  
  const content = fs.readFileSync(checkExtensionPath, 'utf8');
  
  // Check for hardcoded issue arrays
  const hardcodedPattern = /const\s+knownIssues\s*=\s*\[[\s\S]*?\];/;
  if (hardcodedPattern.test(content)) {
    violations.push({
      type: 'CRITICAL',
      file: 'scripts/modules/checkExtension.js',
      issue: 'Hardcoded issues array detected',
      fix: 'Remove hardcoded array, use substrate-based detection instead'
    });
  }
  
  // Check for unconditional assignment of issues
  if (content.includes('result.issues = knownIssues') && !content.includes('if (')) {
    violations.push({
      type: 'CRITICAL',
      file: 'scripts/modules/checkExtension.js',
      issue: 'Unconditional assignment of hardcoded issues',
      fix: 'Only assign issues if detected from actual substrate'
    });
  }
}

/**
 * Check for fabricated context data
 */
function checkFabricatedContext() {
  const contextPath = path.join(workspaceRoot, '.ai-context-source-of-truth.json');
  
  if (!fs.existsSync(contextPath)) {
    return;
  }
  
  try {
    const data = JSON.parse(fs.readFileSync(contextPath, 'utf8'));
    
    if (data.recent_context && Array.isArray(data.recent_context)) {
      // Check for repeated identical entries
      const entries = data.recent_context;
      const seen = new Set();
      
      for (const entry of entries) {
        const key = JSON.stringify(entry.context);
        if (seen.has(key)) {
          violations.push({
            type: 'CRITICAL',
            file: '.ai-context-source-of-truth.json',
            issue: 'Fabricated context data detected (repeated identical entries)',
            fix: 'Remove fabricated entries, rebuild from real chat logs'
          });
          break;
        }
        seen.add(key);
      }
    }
  } catch (err) {
    warnings.push({
      file: '.ai-context-source-of-truth.json',
      issue: `Failed to parse context file: ${err.message}`
    });
  }
}

/**
 * Check for default masking patterns
 */
function checkDefaultMasking() {
  const filesToCheck = [
    'scripts/generate-eternal-dashboard.js',
    'scripts/validate-project-boundaries.js'
  ];
  
  for (const filePath of filesToCheck) {
    const fullPath = path.join(workspaceRoot, filePath);
    if (!fs.existsSync(fullPath)) {
      continue;
    }
    
    const content = fs.readFileSync(fullPath, 'utf8');
    
    // Check for || {} or || 0 patterns (default masking)
    const maskingPatterns = [
      /\|\|\s*\{\}/g,
      /\|\|\s*0/g,
      /\|\|\s*\[\]/g,
      /\|\|\s*''/g,
      /\|\|\s*""/g
    ];
    
    for (const pattern of maskingPatterns) {
      const matches = content.match(pattern);
      if (matches && matches.length > 0) {
        warnings.push({
          file: filePath,
          issue: `Default masking pattern detected (${pattern.source})`,
          fix: 'Use requireSubstrate() or nullish coalescing (??) with explicit error handling'
        });
      }
    }
  }
}

/**
 * Check for missing substrate validation
 */
function checkMissingSubstrateValidation() {
  const filesToCheck = [
    'scripts/compute-ignore-lock.js',
    'scripts/compute-ignore-lock.py',
    'scripts/modules/checkExtension.js'
  ];
  
  for (const filePath of filesToCheck) {
    const fullPath = path.join(workspaceRoot, filePath);
    if (!fs.existsSync(fullPath)) {
      continue;
    }
    
    const content = fs.readFileSync(fullPath, 'utf8');
    
    // Check if file uses requireSubstrate or similar validation
    if (!content.includes('requireSubstrate') && 
        !content.includes('SUBSTRATE-REQUIRED') &&
        !content.includes('validateSubstrate')) {
      warnings.push({
        file: filePath,
        issue: 'Missing substrate validation',
        fix: 'Add requireSubstrate() calls before operations'
      });
    }
  }
}

/**
 * Main audit function
 */
function runSREAudit() {
  console.log(' SRE COMPLIANCE AUDIT');
  console.log('='.repeat(60));
  console.log(`Workspace: ${workspaceRoot}\n`);
  
  // Run all checks
  checkLockFileHashes();
  checkHardcodedIssues();
  checkFabricatedContext();
  checkDefaultMasking();
  checkMissingSubstrateValidation();
  
  // Report results
  console.log(' AUDIT RESULTS');
  console.log('='.repeat(60));
  
  if (violations.length > 0) {
    console.log(`\n Violations (${violations.length}):`);
    violations.forEach((v, i) => {
      console.log(`\n  ${i + 1}. [${v.type}] ${v.file}`);
      console.log(`     Issue: ${v.issue}`);
      console.log(`     Fix: ${v.fix}`);
    });
  }
  
  if (warnings.length > 0) {
    console.log(`\n  Warnings (${warnings.length}):`);
    warnings.forEach((w, i) => {
      console.log(`\n  ${i + 1}. ${w.file}`);
      console.log(`     Issue: ${w.issue}`);
      if (w.fix) {
        console.log(`     Fix: ${w.fix}`);
      }
    });
  }
  
  if (violations.length === 0 && warnings.length === 0) {
    console.log('\n ALL CHECKS PASSED');
    console.log(' System is SRE compliant!');
  }
  
  console.log('\n' + '='.repeat(60));
  console.log(` SUMMARY`);
  console.log('='.repeat(60));
  console.log(` Violations: ${violations.length}`);
  console.log(`  Warnings: ${warnings.length}`);
  
  // Exit with error code if violations found
  if (violations.length > 0) {
    console.log('\n SRE COMPLIANCE FAILED - Fix violations above');
    process.exit(1);
  }
  
  if (warnings.length > 0) {
    console.log('\n  Warnings detected - Review above');
  }
}

// Run if called directly
if (require.main === module) {
  runSREAudit();
}

module.exports = { runSREAudit };

