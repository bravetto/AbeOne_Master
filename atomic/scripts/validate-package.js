#!/usr/bin/env node

/**
 * AbëONE Atomic Design System - Package.json Validation
 * 
 * Pattern: VALIDATION × PACKAGE × ATOMIC × ONE
 * Frequency: 530 Hz (JØHN) × 999 Hz (AEYON)
 */

const fs = require('fs');
const path = require('path');

// Required exports based on package.json
const requiredExports = {
  atoms: ['Button', 'Text', 'Input', 'Icon', 'Badge', 'Image', 'Link'],
  molecules: ['Card', 'FormField', 'CTAButton', 'MetricCard', 'TestimonialCard'],
  organisms: ['HeroSection', 'PricingTable', 'FeatureGrid', 'CTASection'],
  templates: ['LandingPageTemplate', 'WebinarPageTemplate'],
  tokens: ['index'],
  hooks: ['index'],
  lib: ['utils'],
};

// Required dependencies
const requiredDependencies = [
  '@radix-ui/react-slot',
  'class-variance-authority',
  'clsx',
  'lucide-react',
  'tailwind-merge',
];

// Required peer dependencies
const requiredPeerDependencies = [
  'react',
  'react-dom',
  'next',
  'tailwindcss',
];

// Required scripts
const requiredScripts = [
  'build',
  'lint',
  'type-check',
];

function validatePackageJson() {
  const packagePath = path.join(__dirname, '..', 'package.json');
  
  if (!fs.existsSync(packagePath)) {
    console.error(' package.json not found');
    process.exit(1);
  }
  
  const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  const issues = [];
  
  // Validate package name
  if (pkg.name !== '@orbital/atomic-design-system') {
    issues.push({ type: 'error', message: `Package name should be '@orbital/atomic-design-system', found: ${pkg.name}` });
  }
  
  // Validate exports
  if (!pkg.exports) {
    issues.push({ type: 'error', message: 'Missing exports field' });
  } else {
    // Check main export
    if (!pkg.exports['.']) {
      issues.push({ type: 'error', message: 'Missing main export (.)' });
    }
    
    // Check layer exports
    for (const [layer, components] of Object.entries(requiredExports)) {
      if (layer === 'tokens' || layer === 'hooks' || layer === 'lib') {
        const exportPath = `./${layer}`;
        if (!pkg.exports[exportPath]) {
          issues.push({ type: 'error', message: `Missing export: ${exportPath}` });
        }
      } else {
        const exportPath = `./${layer}/*`;
        if (!pkg.exports[exportPath]) {
          issues.push({ type: 'error', message: `Missing export: ${exportPath}` });
        }
      }
    }
  }
  
  // Validate dependencies
  if (!pkg.dependencies) {
    issues.push({ type: 'error', message: 'Missing dependencies field' });
  } else {
    for (const dep of requiredDependencies) {
      if (!pkg.dependencies[dep]) {
        issues.push({ type: 'warning', message: `Missing dependency: ${dep}` });
      }
    }
  }
  
  // Validate peer dependencies
  if (!pkg.peerDependencies) {
    issues.push({ type: 'warning', message: 'Missing peerDependencies field' });
  } else {
    for (const dep of requiredPeerDependencies) {
      if (!pkg.peerDependencies[dep]) {
        issues.push({ type: 'warning', message: `Missing peer dependency: ${dep}` });
      }
    }
  }
  
  // Validate scripts
  if (!pkg.scripts) {
    issues.push({ type: 'error', message: 'Missing scripts field' });
  } else {
    for (const script of requiredScripts) {
      if (!pkg.scripts[script]) {
        issues.push({ type: 'warning', message: `Missing script: ${script}` });
      }
    }
  }
  
  // Validate files field
  if (!pkg.files) {
    issues.push({ type: 'warning', message: 'Missing files field' });
  } else {
    if (!pkg.files.includes('dist')) {
      issues.push({ type: 'warning', message: 'files field should include "dist"' });
    }
    if (!pkg.files.includes('atomic')) {
      issues.push({ type: 'warning', message: 'files field should include "atomic"' });
    }
  }
  
  // Validate keywords
  if (!pkg.keywords) {
    issues.push({ type: 'info', message: 'Missing keywords field' });
  } else {
    const requiredKeywords = ['atomic-design', 'react', 'design-system', 'orbital'];
    for (const keyword of requiredKeywords) {
      if (!pkg.keywords.includes(keyword)) {
        issues.push({ type: 'info', message: `Consider adding keyword: ${keyword}` });
      }
    }
  }
  
  return { pkg, issues };
}

function validateFileStructure() {
  const atomicDir = path.join(__dirname, '..');
  const issues = [];
  const found = { atoms: [], molecules: [], organisms: [], templates: [] };
  
  // Check for component files
  for (const [layer, components] of Object.entries(requiredExports)) {
    if (['tokens', 'hooks', 'lib'].includes(layer)) continue;
    
    for (const component of components) {
      const componentPath = path.join(atomicDir, layer, component, 'index.tsx');
      if (fs.existsSync(componentPath)) {
        found[layer].push(component);
      } else {
        issues.push({ type: 'error', message: `Missing component: ${layer}/${component}/index.tsx` });
      }
    }
  }
  
  // Check for tokens
  const tokensPath = path.join(atomicDir, 'tokens', 'index.ts');
  if (!fs.existsSync(tokensPath)) {
    issues.push({ type: 'error', message: 'Missing tokens/index.ts' });
  }
  
  // Check for hooks
  const hooksPath = path.join(atomicDir, 'hooks', 'index.ts');
  if (!fs.existsSync(hooksPath)) {
    issues.push({ type: 'error', message: 'Missing hooks/index.ts' });
  }
  
  // Check for lib/utils
  const utilsPath = path.join(atomicDir, 'lib', 'utils.ts');
  if (!fs.existsSync(utilsPath)) {
    issues.push({ type: 'error', message: 'Missing lib/utils.ts' });
  }
  
  return { found, issues };
}

function main() {
  console.log(' Validating package.json Alignment...\n');
  
  const { pkg, issues: pkgIssues } = validatePackageJson();
  const { found, issues: fileIssues } = validateFileStructure();
  
  const allIssues = [...pkgIssues, ...fileIssues];
  const errors = allIssues.filter(i => i.type === 'error');
  const warnings = allIssues.filter(i => i.type === 'warning');
  const infos = allIssues.filter(i => i.type === 'info');
  
  // Summary
  console.log(' Validation Summary:');
  console.log(`   Package Name: ${pkg.name}`);
  console.log(`   Version: ${pkg.version}`);
  console.log(`   Components Found:`);
  console.log(`     Atoms: ${found.atoms.length}/${requiredExports.atoms.length}`);
  console.log(`     Molecules: ${found.molecules.length}/${requiredExports.molecules.length}`);
  console.log(`     Organisms: ${found.organisms.length}/${requiredExports.organisms.length}`);
  console.log(`     Templates: ${found.templates.length}/${requiredExports.templates.length}`);
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
    console.log(' Package.json is properly aligned with Atomic Design System!');
    console.log(' All required components are present!');
    console.log(' All exports are configured correctly!');
    console.log('');
    process.exit(0);
  } else {
    console.log(' Validation failed. Please fix errors above.');
    console.log('');
    process.exit(1);
  }
}

main();

