#!/usr/bin/env node

/**
 * AbëONE Atomic Design System - Index Validation
 * 
 * Pattern: VALIDATION × INDEX × ATOMIC × ONE
 * Frequency: 530 Hz (JØHN) × 999 Hz (AEYON)
 */

const fs = require('fs');
const path = require('path');

// Expected exports from index.ts
const expectedExports = {
  atoms: ['Button', 'Text', 'Input', 'Icon', 'Badge', 'Image', 'Link'],
  molecules: ['Card', 'FormField', 'CTAButton', 'TestimonialCard', 'MetricCard'],
  organisms: ['HeroSection', 'PricingTable', 'FeatureGrid', 'CTASection'],
  templates: ['LandingPageTemplate', 'WebinarPageTemplate'],
  utilities: ['cn'],
  hooks: ['useICP', 'useOrbital', 'useCTAHierarchy'],
  tokens: ['*'],
};

function validateIndexFile() {
  const indexPath = path.join(__dirname, '..', 'index.ts');
  
  if (!fs.existsSync(indexPath)) {
    console.error(' index.ts not found');
    process.exit(1);
  }
  
  const indexContent = fs.readFileSync(indexPath, 'utf8');
  const issues = [];
  const found = { atoms: [], molecules: [], organisms: [], templates: [], utilities: [], hooks: [] };
  
  // Check atoms
  for (const atom of expectedExports.atoms) {
    if (indexContent.includes(`export { ${atom}`) || indexContent.includes(`export { ${atom},`)) {
      found.atoms.push(atom);
      
      // Check if file exists
      const atomPath = path.join(__dirname, '..', 'atoms', atom, 'index.tsx');
      if (!fs.existsSync(atomPath)) {
        issues.push({ type: 'error', message: `Atom ${atom} exported but file missing: ${atomPath}` });
      }
    } else {
      issues.push({ type: 'error', message: `Missing atom export: ${atom}` });
    }
  }
  
  // Check molecules
  for (const molecule of expectedExports.molecules) {
    if (indexContent.includes(`export { ${molecule}`) || indexContent.includes(`export { ${molecule},`)) {
      found.molecules.push(molecule);
      
      // Check if file exists
      const moleculePath = path.join(__dirname, '..', 'molecules', molecule, 'index.tsx');
      if (!fs.existsSync(moleculePath)) {
        issues.push({ type: 'error', message: `Molecule ${molecule} exported but file missing: ${moleculePath}` });
      }
    } else {
      issues.push({ type: 'error', message: `Missing molecule export: ${molecule}` });
    }
  }
  
  // Check organisms
  for (const organism of expectedExports.organisms) {
    if (indexContent.includes(`export { ${organism}`) || indexContent.includes(`export { ${organism},`)) {
      found.organisms.push(organism);
      
      // Check if file exists
      const organismPath = path.join(__dirname, '..', 'organisms', organism, 'index.tsx');
      if (!fs.existsSync(organismPath)) {
        issues.push({ type: 'error', message: `Organism ${organism} exported but file missing: ${organismPath}` });
      }
    } else {
      issues.push({ type: 'error', message: `Missing organism export: ${organism}` });
    }
  }
  
  // Check templates
  for (const template of expectedExports.templates) {
    if (indexContent.includes(`export { ${template}`) || indexContent.includes(`export { ${template},`)) {
      found.templates.push(template);
      
      // Check if file exists
      const templatePath = path.join(__dirname, '..', 'templates', template, 'index.tsx');
      if (!fs.existsSync(templatePath)) {
        issues.push({ type: 'error', message: `Template ${template} exported but file missing: ${templatePath}` });
      }
    } else {
      issues.push({ type: 'error', message: `Missing template export: ${template}` });
    }
  }
  
  // Check utilities
  if (indexContent.includes('export { cn }')) {
    found.utilities.push('cn');
    const utilsPath = path.join(__dirname, '..', 'lib', 'utils.ts');
    if (!fs.existsSync(utilsPath)) {
      issues.push({ type: 'error', message: 'Utility cn exported but file missing: lib/utils.ts' });
    }
  } else {
    issues.push({ type: 'error', message: 'Missing utility export: cn' });
  }
  
  // Check hooks
  for (const hook of expectedExports.hooks) {
    if (indexContent.includes(`export { ${hook}`) || indexContent.includes(`export { ${hook},`)) {
      found.hooks.push(hook);
    } else {
      issues.push({ type: 'warning', message: `Missing hook export: ${hook}` });
    }
  }
  
  // Check tokens export
  if (!indexContent.includes('export * from \'./tokens\'')) {
    issues.push({ type: 'warning', message: 'Missing tokens export' });
  }
  
  return { indexContent, found, issues };
}

function main() {
  console.log(' Validating Component Index...\n');
  
  const { found, issues } = validateIndexFile();
  
  const errors = issues.filter(i => i.type === 'error');
  const warnings = issues.filter(i => i.type === 'warning');
  
  // Summary
  console.log(' Validation Summary:');
  console.log(`   Atoms: ${found.atoms.length}/${expectedExports.atoms.length}`);
  console.log(`   Molecules: ${found.molecules.length}/${expectedExports.molecules.length}`);
  console.log(`   Organisms: ${found.organisms.length}/${expectedExports.organisms.length}`);
  console.log(`   Templates: ${found.templates.length}/${expectedExports.templates.length}`);
  console.log(`   Utilities: ${found.utilities.length}/${expectedExports.utilities.length}`);
  console.log(`   Hooks: ${found.hooks.length}/${expectedExports.hooks.length}`);
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
    console.log(' Component index is properly aligned with Atomic Design System!');
    console.log(' All exports match existing components!');
    console.log(' All files exist and are accessible!');
    console.log('');
    process.exit(0);
  } else {
    console.log(' Validation failed. Please fix errors above.');
    console.log('');
    process.exit(1);
  }
}

main();

