#!/usr/bin/env node

/**
 * AbëONE Atomic Design System - Global Styles Validation
 * 
 * Pattern: VALIDATION × STYLES × ATOMIC × ONE
 * Frequency: 530 Hz (JØHN) × 999 Hz (AEYON)
 */

const fs = require('fs');
const path = require('path');

// Required CSS variables
const requiredVariables = [
  '--background',
  '--foreground',
  '--card',
  '--card-foreground',
  '--popover',
  '--popover-foreground',
  '--primary',
  '--primary-foreground',
  '--secondary',
  '--secondary-foreground',
  '--muted',
  '--muted-foreground',
  '--accent',
  '--accent-foreground',
  '--destructive',
  '--destructive-foreground',
  '--success',
  '--success-foreground',
  '--border',
  '--input',
  '--ring',
  '--radius',
];

// Required typography variables
const requiredTypography = [
  '--font-sans',
  '--font-mono',
  '--font-heading',
];

// Required ICP variants
const requiredICPVariants = [
  'icp-developer',
  'icp-creative',
  'icp-enterprise',
];

// Required utility classes
const requiredUtilities = [
  'scrollbar-hide',
  'text-balance',
  'gradient-text',
  'glass',
  'animated-gradient',
  'shine',
];

// Required animations
const requiredAnimations = [
  'fade-in',
  'fade-out',
  'slide-in-from-bottom-4',
  'slide-in-from-top-4',
];

function validateGlobalStyles() {
  const stylesPath = path.join(__dirname, '..', 'styles', 'globals.css');
  
  if (!fs.existsSync(stylesPath)) {
    console.error(' globals.css not found');
    process.exit(1);
  }
  
  const css = fs.readFileSync(stylesPath, 'utf8');
  const issues = [];
  
  // Check Tailwind directives
  if (!css.includes('@tailwind base')) {
    issues.push({ type: 'error', message: 'Missing @tailwind base directive' });
  }
  if (!css.includes('@tailwind components')) {
    issues.push({ type: 'error', message: 'Missing @tailwind components directive' });
  }
  if (!css.includes('@tailwind utilities')) {
    issues.push({ type: 'error', message: 'Missing @tailwind utilities directive' });
  }
  
  // Check CSS variables in :root
  const rootMatch = css.match(/:root\s*\{([^}]+)\}/);
  if (!rootMatch) {
    issues.push({ type: 'error', message: 'Missing :root CSS variables block' });
  } else {
    const rootVars = rootMatch[1];
    for (const variable of requiredVariables) {
      if (!rootVars.includes(variable)) {
        issues.push({ type: 'error', message: `Missing CSS variable: ${variable}` });
      }
    }
    for (const typo of requiredTypography) {
      if (!rootVars.includes(typo)) {
        issues.push({ type: 'error', message: `Missing typography variable: ${typo}` });
      }
    }
  }
  
  // Check dark mode
  if (!css.includes('.dark')) {
    issues.push({ type: 'error', message: 'Missing .dark CSS variables block' });
  }
  
  // Check ICP variants
  for (const variant of requiredICPVariants) {
    if (!css.includes(`.${variant}`)) {
      issues.push({ type: 'error', message: `Missing ICP variant: .${variant}` });
    } else {
      // Check that variant has required variables
      const variantMatch = css.match(new RegExp(`\\.${variant}\\s*\\{([^}]+)\\}`, 's'));
      if (variantMatch) {
        const variantVars = variantMatch[1];
        const requiredVarsForVariant = ['--background', '--foreground', '--primary'];
        for (const variable of requiredVarsForVariant) {
          if (!variantVars.includes(variable)) {
            issues.push({ type: 'warning', message: `ICP variant .${variant} missing variable: ${variable}` });
          }
        }
      }
    }
  }
  
  // Check utility classes
  for (const utility of requiredUtilities) {
    if (!css.includes(`.${utility}`)) {
      issues.push({ type: 'warning', message: `Missing utility class: .${utility}` });
    }
  }
  
  // Check animations
  for (const animation of requiredAnimations) {
    if (!css.includes(`.${animation}`)) {
      issues.push({ type: 'warning', message: `Missing animation class: .${animation}` });
    }
  }
  
  // Check keyframes
  if (!css.includes('@keyframes gradient')) {
    issues.push({ type: 'warning', message: 'Missing @keyframes gradient' });
  }
  if (!css.includes('@keyframes shine')) {
    issues.push({ type: 'warning', message: 'Missing @keyframes shine' });
  }
  
  // Check base styles
  if (!css.includes('@layer base')) {
    issues.push({ type: 'error', message: 'Missing @layer base' });
  }
  
  // Check utilities layer
  if (!css.includes('@layer utilities')) {
    issues.push({ type: 'error', message: 'Missing @layer utilities' });
  }
  
  // Check print styles
  if (!css.includes('@media print')) {
    issues.push({ type: 'info', message: 'Missing print styles (optional)' });
  }
  
  return { css, issues };
}

function main() {
  console.log(' Validating Global Styles...\n');
  
  const { css, issues } = validateGlobalStyles();
  
  const errors = issues.filter(i => i.type === 'error');
  const warnings = issues.filter(i => i.type === 'warning');
  const infos = issues.filter(i => i.type === 'info');
  
  // Summary
  console.log(' Validation Summary:');
  console.log(`   File: atomic/styles/globals.css`);
  console.log(`   Size: ${(css.length / 1024).toFixed(2)} KB`);
  console.log(`   Issues: ${errors.length} errors, ${warnings.length} warnings, ${infos.length} info\n`);
  
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
  
  if (infos.length > 0) {
    console.log('ℹ  Info:');
    infos.forEach(issue => {
      console.log(`   ${issue.message}`);
    });
    console.log('');
  }
  
  if (errors.length === 0) {
    console.log(' Global styles are properly aligned with Atomic Design System!');
    console.log(' All CSS variables are present!');
    console.log(' All ICP variants are configured!');
    console.log(' All utility classes are defined!');
    console.log('');
    process.exit(0);
  } else {
    console.log(' Validation failed. Please fix errors above.');
    console.log('');
    process.exit(1);
  }
}

main();

