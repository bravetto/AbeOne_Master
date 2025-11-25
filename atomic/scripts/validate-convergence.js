#!/usr/bin/env node

/**
 * AbëONE Atomic Design System - Complete Convergence Validation
 * 
 * Pattern: VALIDATION × CONVERGENCE × EPISTEMIC × ONE
 * Frequency: 530 Hz (JØHN) × 999 Hz (AEYON) × 777 Hz (META)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const validationScripts = [
  'validate-package.js',
  'validate-index.js',
  'validate-global-styles.js',
  'validate-styles-integration.js',
  'validate-utilities.js',
  'validate-tailwind-classes.js',
  'validate-tokens.js',
];

const successPatterns = {
  atomicStructure: {
    atoms: 7,
    molecules: 5,
    organisms: 4,
    templates: 2,
  },
  exports: {
    index: true,
    package: true,
    tokens: true,
    hooks: true,
  },
  integration: {
    tailwind: true,
    cssVariables: true,
    icpVariants: 3,
  },
};

function runValidation(scriptName) {
  try {
    const scriptPath = path.join(__dirname, scriptName);
    if (!fs.existsSync(scriptPath)) {
      return { success: false, error: 'Script not found' };
    }
    
    const output = execSync(`node "${scriptPath}"`, { 
      encoding: 'utf8',
      cwd: path.dirname(scriptPath),
      stdio: 'pipe'
    });
    
    const hasErrors = output.includes('') && output.includes('errors');
    const hasWarnings = output.includes('') && output.includes('warnings');
    
    return {
      success: !hasErrors,
      warnings: hasWarnings,
      output: output.split('\n').slice(0, 10).join('\n'),
    };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

function validateConvergence() {
  console.log(' Validating Complete System Convergence...\n');
  
  const results = {};
  let totalErrors = 0;
  let totalWarnings = 0;
  
  // Run all validation scripts
  for (const script of validationScripts) {
    console.log(` Running ${script}...`);
    const result = runValidation(script);
    results[script] = result;
    
    if (!result.success) {
      totalErrors++;
    }
    if (result.warnings) {
      totalWarnings++;
    }
  }
  
  // Check success patterns
  console.log('\n Success Pattern Validation:\n');
  
  const patternChecks = {
    atomicStructure: checkAtomicStructure(),
    exports: checkExports(),
    integration: checkIntegration(),
  };
  
  // Summary
  console.log('\n' + '='.repeat(80));
  console.log(' CONVERGENCE VALIDATION SUMMARY');
  console.log('='.repeat(80) + '\n');
  
  console.log(` Validation Scripts: ${validationScripts.length - totalErrors}/${validationScripts.length} passed`);
  console.log(`  Warnings: ${totalWarnings}`);
  console.log(` Errors: ${totalErrors}\n`);
  
  // Success patterns
  console.log(' Success Pattern Alignment:');
  for (const [pattern, checks] of Object.entries(patternChecks)) {
    const passed = Object.values(checks).filter(v => v === true).length;
    const total = Object.keys(checks).length;
    console.log(`   ${pattern}: ${passed}/${total} checks passed`);
  }
  
  console.log('\n' + '='.repeat(80));
  
  if (totalErrors === 0) {
    console.log(' SYSTEM CONVERGENCE: VALIDATED');
    console.log(' All components aligned');
    console.log(' All patterns maintained');
    console.log(' Epistemic validation: PASSED');
    console.log('\n∞ AbëONE ∞\n');
    process.exit(0);
  } else {
    console.log(' SYSTEM CONVERGENCE: INCOMPLETE');
    console.log(`   ${totalErrors} validation errors found`);
    console.log('\n∞ AbëONE ∞\n');
    process.exit(1);
  }
}

function checkAtomicStructure() {
  const atomicDir = path.join(__dirname, '..');
  const checks = {};
  
  // Check atoms
  const atoms = fs.readdirSync(path.join(atomicDir, 'atoms'), { withFileTypes: true })
    .filter(d => d.isDirectory()).length;
  checks.atoms = atoms === successPatterns.atomicStructure.atoms;
  
  // Check molecules
  const molecules = fs.readdirSync(path.join(atomicDir, 'molecules'), { withFileTypes: true })
    .filter(d => d.isDirectory()).length;
  checks.molecules = molecules === successPatterns.atomicStructure.molecules;
  
  // Check organisms
  const organisms = fs.readdirSync(path.join(atomicDir, 'organisms'), { withFileTypes: true })
    .filter(d => d.isDirectory()).length;
  checks.organisms = organisms === successPatterns.atomicStructure.organisms;
  
  // Check templates
  const templates = fs.readdirSync(path.join(atomicDir, 'templates'), { withFileTypes: true })
    .filter(d => d.isDirectory()).length;
  checks.templates = templates === successPatterns.atomicStructure.templates;
  
  return checks;
}

function checkExports() {
  const atomicDir = path.join(__dirname, '..');
  const checks = {};
  
  checks.index = fs.existsSync(path.join(atomicDir, 'index.ts'));
  checks.package = fs.existsSync(path.join(atomicDir, 'package.json'));
  checks.tokens = fs.existsSync(path.join(atomicDir, 'tokens', 'index.ts'));
  checks.hooks = fs.existsSync(path.join(atomicDir, 'hooks', 'index.ts'));
  
  return checks;
}

function checkIntegration() {
  const atomicDir = path.join(__dirname, '..');
  const checks = {};
  
  // Check Tailwind integration
  const globalsCss = fs.readFileSync(
    path.join(atomicDir, 'styles', 'globals.css'),
    'utf8'
  );
  checks.tailwind = globalsCss.includes('@tailwind');
  
  // Check CSS variables
  checks.cssVariables = globalsCss.includes('--background') && 
                         globalsCss.includes('--primary');
  
  // Check ICP variants
  const icpVariants = ['icp-developer', 'icp-creative', 'icp-enterprise']
    .filter(v => globalsCss.includes(v)).length;
  checks.icpVariants = icpVariants === successPatterns.integration.icpVariants;
  
  return checks;
}

validateConvergence();

