#!/usr/bin/env node

/**
 * AbëONE Atomic Design System - Design Tokens Validation
 * 
 * Pattern: VALIDATION × TOKENS × ATOMIC × ONE
 * Frequency: 530 Hz (JØHN) × 999 Hz (AEYON)
 */

const fs = require('fs');
const path = require('path');

// Required token groups
const requiredTokenGroups = [
  'colors',
  'typography',
  'spacing',
  'borderRadius',
  'animation',
  'shadows',
  'breakpoints',
  'zIndex',
];

// Required color tokens
const requiredColors = [
  'primary',
  'secondary',
  'accent',
  'destructive',
  'success',
  'muted',
  'background',
  'foreground',
  'card',
  'popover',
  'border',
  'input',
  'ring',
];

// Required typography tokens
const requiredTypography = [
  'fontFamily',
  'fontSize',
  'fontWeight',
];

// Required exports
const requiredExports = [
  'tokens',
  'colors',
  'typography',
  'spacing',
  'borderRadius',
  'animation',
  'shadows',
  'breakpoints',
  'zIndex',
  'Tokens',
  'ColorToken',
  'SpacingToken',
  'FontSizeToken',
  'ICPVariant',
];

function validateTokens() {
  const tokensPath = path.join(__dirname, '..', 'tokens', 'index.ts');
  
  if (!fs.existsSync(tokensPath)) {
    console.error(' tokens/index.ts not found');
    process.exit(1);
  }
  
  const tokensContent = fs.readFileSync(tokensPath, 'utf8');
  const issues = [];
  
  // Check token groups
  for (const group of requiredTokenGroups) {
    if (!tokensContent.includes(`${group}:`)) {
      issues.push({ type: 'error', message: `Missing token group: ${group}` });
    }
  }
  
  // Check color tokens
  for (const color of requiredColors) {
    if (!tokensContent.includes(`${color}:`)) {
      issues.push({ type: 'error', message: `Missing color token: ${color}` });
    }
  }
  
  // Check typography tokens
  for (const typo of requiredTypography) {
    if (!tokensContent.includes(`${typo}:`)) {
      issues.push({ type: 'error', message: `Missing typography token: ${typo}` });
    }
  }
  
  // Check exports
  for (const exp of requiredExports) {
    if (exp === 'Tokens' || exp === 'ColorToken' || exp === 'SpacingToken' || exp === 'FontSizeToken' || exp === 'ICPVariant') {
      // Type exports
      if (!tokensContent.includes(`export type ${exp}`)) {
        issues.push({ type: 'warning', message: `Missing type export: ${exp}` });
      }
    } else if (exp === 'tokens') {
      // Main tokens export
      if (!tokensContent.includes(`export const tokens`) && !tokensContent.includes(`export const tokens =`)) {
        issues.push({ type: 'error', message: `Missing export: ${exp}` });
      }
    } else {
      // Destructured exports (colors, typography, etc.)
      if (!tokensContent.includes(`export const { ${exp}`) && 
          !tokensContent.includes(`export const ${exp}`) && 
          !tokensContent.includes(`export { ${exp}`)) {
        // Check if it's in the destructured export list
        const destructuredMatch = tokensContent.match(/export const \{([^}]+)\}/);
        if (!destructuredMatch || !destructuredMatch[1].includes(exp)) {
          issues.push({ type: 'error', message: `Missing export: ${exp}` });
        }
      }
    }
  }
  
  // Check CSS variable references
  if (!tokensContent.includes('hsl(var(--')) {
    issues.push({ type: 'warning', message: 'No CSS variable references found (colors should use CSS variables)' });
  }
  
  return { tokensContent, issues };
}

function main() {
  console.log(' Validating Design Tokens...\n');
  
  const { tokensContent, issues } = validateTokens();
  
  const errors = issues.filter(i => i.type === 'error');
  const warnings = issues.filter(i => i.type === 'warning');
  
  // Summary
  console.log(' Validation Summary:');
  console.log(`   File: tokens/index.ts`);
  console.log(`   Size: ${(tokensContent.length / 1024).toFixed(2)} KB`);
  console.log(`   Token Groups: ${requiredTokenGroups.length} required`);
  console.log(`   Color Tokens: ${requiredColors.length} required`);
  console.log(`   Typography Tokens: ${requiredTypography.length} required`);
  console.log(`   Exports: ${requiredExports.length} required`);
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
    console.log(' Design tokens are properly aligned with Atomic Design System!');
    console.log(' All token groups are present!');
    console.log(' All color tokens are defined!');
    console.log(' All typography tokens are defined!');
    console.log(' All exports are configured!');
    console.log('');
    process.exit(0);
  } else {
    console.log(' Validation failed. Please fix errors above.');
    console.log('');
    process.exit(1);
  }
}

main();

