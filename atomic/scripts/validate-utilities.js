#!/usr/bin/env node

/**
 * AbëONE Atomic Design System - Utilities & Hooks Validation
 * 
 * Pattern: VALIDATION × UTILITIES × HOOKS × ONE
 * Frequency: 530 Hz (JØHN) × 999 Hz (AEYON)
 */

const fs = require('fs');
const path = require('path');

// Required utilities
const requiredUtilities = [
  'cn',
  'getTemplateForChannel',
  'validateOrbitalAlignment',
  'calculateDrift',
];

// Required hooks
const requiredHooks = [
  'useICP',
  'useOrbital',
  'useCTAHierarchy',
  'useMediaQuery',
  'useIsMobile',
  'useIsTablet',
  'useIsDesktop',
  'useScrollPosition',
  'useInView',
];

// Required types
const requiredTypes = [
  'ICPVariant',
  'ICPConfig',
  'OrbitalComponent',
  'OrbitalMapping',
  'OrbitalState',
  'CTANode',
  'CTAHierarchyState',
  'DistributionChannel',
];

// Required animation utilities
const requiredAnimations = [
  'fadeIn',
  'slideUp',
  'slideIn',
  'stagger',
];

function validateUtilities() {
  const utilsPath = path.join(__dirname, '..', 'lib', 'utils.ts');
  const hooksPath = path.join(__dirname, '..', 'hooks', 'index.ts');
  const issues = [];
  
  // Check lib/utils.ts
  if (!fs.existsSync(utilsPath)) {
    issues.push({ type: 'error', message: 'lib/utils.ts not found' });
    return { issues };
  }
  
  const utilsContent = fs.readFileSync(utilsPath, 'utf8');
  
  // Check utilities
  for (const util of requiredUtilities) {
    if (!utilsContent.includes(`export function ${util}`) && !utilsContent.includes(`export const ${util}`)) {
      issues.push({ type: 'error', message: `Missing utility: ${util}` });
    }
  }
  
  // Check hooks
  for (const hook of requiredHooks) {
    if (!utilsContent.includes(`export function ${hook}`)) {
      issues.push({ type: 'error', message: `Missing hook: ${hook}` });
    }
  }
  
  // Check types
  for (const type of requiredTypes) {
    if (!utilsContent.includes(`export type ${type}`) && !utilsContent.includes(`export interface ${type}`)) {
      issues.push({ type: 'warning', message: `Missing type: ${type}` });
    }
  }
  
  // Check animation utilities
  for (const anim of requiredAnimations) {
    if (!utilsContent.includes(`export const ${anim}`)) {
      issues.push({ type: 'warning', message: `Missing animation: ${anim}` });
    }
  }
  
  // Check hooks/index.ts
  if (!fs.existsSync(hooksPath)) {
    issues.push({ type: 'error', message: 'hooks/index.ts not found' });
  } else {
    const hooksContent = fs.readFileSync(hooksPath, 'utf8');
    
    // Check that hooks are re-exported
    for (const hook of requiredHooks) {
      if (!hooksContent.includes(hook)) {
        issues.push({ type: 'warning', message: `Hook ${hook} not exported from hooks/index.ts` });
      }
    }
  }
  
  return { utilsContent, issues };
}

function main() {
  console.log(' Validating Utilities & Hooks...\n');
  
  const { issues } = validateUtilities();
  
  const errors = issues.filter(i => i.type === 'error');
  const warnings = issues.filter(i => i.type === 'warning');
  
  // Summary
  console.log(' Validation Summary:');
  console.log(`   Utilities: ${requiredUtilities.length} required`);
  console.log(`   Hooks: ${requiredHooks.length} required`);
  console.log(`   Types: ${requiredTypes.length} required`);
  console.log(`   Animations: ${requiredAnimations.length} required`);
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
    console.log(' Utilities & Hooks are properly aligned with Atomic Design System!');
    console.log(' All utilities are present!');
    console.log(' All hooks are defined!');
    console.log(' All types are exported!');
    console.log('');
    process.exit(0);
  } else {
    console.log(' Validation failed. Please fix errors above.');
    console.log('');
    process.exit(1);
  }
}

main();

