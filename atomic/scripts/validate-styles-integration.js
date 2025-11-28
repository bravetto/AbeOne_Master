#!/usr/bin/env node

/**
 * AbëONE Atomic Design System - Styles Integration Validation
 * 
 * Pattern: VALIDATION × STYLES × INTEGRATION × ATOMIC × ONE
 * Frequency: 530 Hz (JØHN) × 999 Hz (AEYON)
 */

const fs = require('fs');
const path = require('path');

function validateStylesIntegration() {
  const issues = [];
  const checks = {
    globalsExists: false,
    tailwindConfigExists: false,
    icpVariantsInComponents: false,
    cssVariablesUsed: false,
  };
  
  // Check globals.css exists
  const globalsPath = path.join(__dirname, '..', 'styles', 'globals.css');
  if (fs.existsSync(globalsPath)) {
    checks.globalsExists = true;
    const globalsContent = fs.readFileSync(globalsPath, 'utf8');
    
    // Check ICP variants are defined
    if (globalsContent.includes('.icp-developer') && 
        globalsContent.includes('.icp-creative') && 
        globalsContent.includes('.icp-enterprise')) {
      checks.icpVariantsInStyles = true;
    } else {
      issues.push({ type: 'error', message: 'ICP variants missing in globals.css' });
    }
    
    // Check CSS variables are defined
    if (globalsContent.includes('--background') && 
        globalsContent.includes('--primary') && 
        globalsContent.includes('--radius')) {
      checks.cssVariablesUsed = true;
    } else {
      issues.push({ type: 'error', message: 'CSS variables missing in globals.css' });
    }
  } else {
    issues.push({ type: 'error', message: 'globals.css not found' });
  }
  
  // Check if components use ICP variants
  const atomsPath = path.join(__dirname, '..', 'atoms');
  if (fs.existsSync(atomsPath)) {
    const atoms = fs.readdirSync(atomsPath, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .map(dirent => dirent.name);
    
    let componentsWithVariants = 0;
    for (const atom of atoms) {
      const atomFile = path.join(atomsPath, atom, 'index.tsx');
      if (fs.existsSync(atomFile)) {
        const content = fs.readFileSync(atomFile, 'utf8');
        if (content.includes('variant') && content.includes('developer')) {
          componentsWithVariants++;
        }
      }
    }
    
    if (componentsWithVariants > 0) {
      checks.icpVariantsInComponents = true;
    } else {
      issues.push({ type: 'warning', message: 'No components found using ICP variants' });
    }
  }
  
  // Check Tailwind config alignment
  const tailwindConfigPath = path.join(__dirname, '..', '..', 'products', 'apps', 'web', 'tailwind.config.ts');
  const tailwindConfigJsPath = path.join(__dirname, '..', '..', 'products', 'apps', 'web', 'tailwind.config.js');
  
  if (fs.existsSync(tailwindConfigPath) || fs.existsSync(tailwindConfigJsPath)) {
    checks.tailwindConfigExists = true;
    const configPath = fs.existsSync(tailwindConfigPath) ? tailwindConfigPath : tailwindConfigJsPath;
    const configContent = fs.readFileSync(configPath, 'utf8');
    
    // Check if atomic directory is in content paths
    if (configContent.includes('./atomic') || configContent.includes('atomic/**')) {
      checks.atomicInTailwind = true;
    } else {
      issues.push({ type: 'warning', message: 'Atomic directory not found in Tailwind content paths' });
    }
  } else {
    issues.push({ type: 'warning', message: 'Tailwind config not found (may be in different location)' });
  }
  
  return { checks, issues };
}

function main() {
  console.log(' Validating Styles Integration...\n');
  
  const { checks, issues } = validateStylesIntegration();
  
  const errors = issues.filter(i => i.type === 'error');
  const warnings = issues.filter(i => i.type === 'warning');
  
  // Summary
  console.log(' Integration Summary:');
  console.log(`   Global Styles: ${checks.globalsExists ? '' : ''}`);
  console.log(`   ICP Variants: ${checks.icpVariantsInStyles ? '' : ''}`);
  console.log(`   CSS Variables: ${checks.cssVariablesUsed ? '' : ''}`);
  console.log(`   Components Using Variants: ${checks.icpVariantsInComponents ? '' : ''}`);
  console.log(`   Tailwind Config: ${checks.tailwindConfigExists ? '' : ''}`);
  console.log(`   Issues: ${errors.length} errors, ${warnings.length} warnings\n`);
  
  // Issues
  if (errors.length > 0) {
    console.log(' Errors:');
    errors.forEach(issue => {
      console.log(`   ${issue.message}`);
    });
    console.log('');
  }
  
  if (warnings.length > 0) {
    console.log('  Warnings:');
    warnings.forEach(issue => {
      console.log(`   ${issue.message}`);
    });
    console.log('');
  }
  
  if (errors.length === 0) {
    console.log(' Styles are properly integrated with Atomic Design System!');
    console.log(' Global styles aligned with components!');
    console.log(' ICP variants configured correctly!');
    console.log('');
    process.exit(0);
  } else {
    console.log(' Validation failed. Please fix errors above.');
    console.log('');
    process.exit(1);
  }
}

main();

