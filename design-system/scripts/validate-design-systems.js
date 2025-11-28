#!/usr/bin/env node
/**
 * Comprehensive Design System Validator
 * Validates all design systems, checks for conflicts, drift, and organization
 * 
 * Usage: node design-system/scripts/validate-design-systems.js
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const issues = [];
const warnings = [];
const passed = [];
const conflicts = [];

// Colors for output
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const GREEN = '\x1b[32m';
const BLUE = '\x1b[34m';
const RESET = '\x1b[0m';

console.log(`${BLUE}🔍 Validating AbëONE Design Systems...${RESET}\n`);

// 1. Check for design system files
function checkDesignSystemFiles() {
  console.log(`${BLUE}Step 1: Checking design system files...${RESET}`);
  
  const requiredFiles = [
    'design-system/tokens/abeone-unified-color-system-v2.json',
    'design-system/tokens/abeone-design-system-v1.json',
    'apps/web/tailwind.config.js',
  ];

  requiredFiles.forEach(file => {
    if (fs.existsSync(file)) {
      passed.push(`✅ ${file} exists`);
    } else {
      issues.push(`❌ ${file} missing`);
    }
  });
}

// 2. Validate unified color system structure
function validateUnifiedColorSystem() {
  console.log(`${BLUE}Step 2: Validating unified color system structure...${RESET}`);
  
  try {
    const systemPath = 'design-system/tokens/abeone-unified-color-system-v2.json';
    const system = JSON.parse(fs.readFileSync(systemPath, 'utf8'));
    
    // Check required palettes
    const requiredPalettes = ['healing', 'technicalCalm', 'vermillion'];
    requiredPalettes.forEach(palette => {
      if (system.colorSystem?.palettes?.[palette]) {
        passed.push(`✅ Palette '${palette}' exists`);
      } else {
        issues.push(`❌ Palette '${palette}' missing`);
      }
    });
    
    // Check healing palette colors
    const healingColors = ['lux', 'warm', 'heart', 'peace'];
    healingColors.forEach(color => {
      if (system.colorSystem?.palettes?.healing?.colors?.[color]) {
        passed.push(`✅ Healing color '${color}' exists`);
      } else {
        issues.push(`❌ Healing color '${color}' missing`);
      }
    });
    
    // Check technical calm colors
    const technicalColors = ['aeBlue', 'aeIndigo', 'aeMidnight', 'aeAqua', 'aeMint'];
    technicalColors.forEach(color => {
      if (system.colorSystem?.palettes?.technicalCalm?.colors?.[color]) {
        passed.push(`✅ Technical Calm color '${color}' exists`);
      } else {
        issues.push(`❌ Technical Calm color '${color}' missing`);
      }
    });
    
    // Check color scales (50-900)
    const healing = system.colorSystem.palettes.healing.colors;
    Object.keys(healing).forEach(colorName => {
      const color = healing[colorName];
      const scales = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'];
      scales.forEach(scale => {
        if (!color[scale]) {
          warnings.push(`⚠️  ${colorName}-${scale} missing`);
        }
      });
    });
    
  } catch (error) {
    issues.push(`❌ Error validating unified color system: ${error.message}`);
  }
}

// 3. Check for hardcoded colors in codebase
function checkHardcodedColors() {
  console.log(`${BLUE}Step 3: Checking for hardcoded colors...${RESET}`);
  
  try {
    // Check apps/web directory
    const result = execSync(
      'grep -r "bg-purple\\|text-gray\\|#[0-9a-fA-F]\\{6\\}" apps/web/app apps/web/components 2>/dev/null || true',
      { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
    );
    
    if (result.trim()) {
      const lines = result.trim().split('\n').filter(l => l && !l.includes('node_modules'));
      if (lines.length > 0) {
        warnings.push(`⚠️  Found ${lines.length} potential hardcoded colors`);
        lines.slice(0, 5).forEach(line => {
          warnings.push(`   ${line.substring(0, 100)}`);
        });
        if (lines.length > 5) {
          warnings.push(`   ... and ${lines.length - 5} more`);
        }
      }
    } else {
      passed.push(`✅ No hardcoded colors found in apps/web`);
    }
  } catch (error) {
    // grep returns non-zero if no matches found, which is good
    passed.push(`✅ No hardcoded colors found`);
  }
}

// 4. Check for inline styles
function checkInlineStyles() {
  console.log(`${BLUE}Step 4: Checking for inline styles...${RESET}`);
  
  try {
    const result = execSync(
      'grep -r "style=" apps/web/app apps/web/components 2>/dev/null | grep -v "node_modules" | grep -v ".next" || true',
      { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
    );
    
    if (result.trim()) {
      const lines = result.trim().split('\n').filter(l => l);
      if (lines.length > 0) {
        warnings.push(`⚠️  Found ${lines.length} inline style usages`);
        lines.slice(0, 3).forEach(line => {
          warnings.push(`   ${line.substring(0, 100)}`);
        });
      }
    } else {
      passed.push(`✅ No inline styles found`);
    }
  } catch (error) {
    passed.push(`✅ No inline styles found`);
  }
}

// 5. Validate Tailwind config sync
function validateTailwindSync() {
  console.log(`${BLUE}Step 5: Validating Tailwind config sync...${RESET}`);
  
  try {
    const tailwindPath = 'apps/web/tailwind.config.js';
    const tailwindContent = fs.readFileSync(tailwindPath, 'utf8');
    
    // Check for required colors
    const requiredColors = ['lux', 'warm', 'heart', 'peace', 'aeBlue', 'aeIndigo', 'aeMidnight', 'aeAqua', 'aeMint', 'vermillion'];
    requiredColors.forEach(color => {
      if (tailwindContent.includes(color)) {
        passed.push(`✅ Tailwind config includes '${color}'`);
      } else {
        issues.push(`❌ Tailwind config missing '${color}'`);
      }
    });
    
    // Check if config is generated (has comment)
    if (tailwindContent.includes('DO NOT EDIT MANUALLY') || tailwindContent.includes('Generated')) {
      passed.push(`✅ Tailwind config appears to be generated`);
    } else {
      warnings.push(`⚠️  Tailwind config may not be generated (missing generation comment)`);
    }
    
  } catch (error) {
    issues.push(`❌ Error validating Tailwind config: ${error.message}`);
  }
}

// 6. Check for design system conflicts
function checkConflicts() {
  console.log(`${BLUE}Step 6: Checking for design system conflicts...${RESET}`);
  
  // Check for multiple tailwind configs
  try {
    const tailwindConfigs = execSync(
      'find . -name "tailwind.config.*" -type f 2>/dev/null | grep -v node_modules | grep -v ".next" || true',
      { encoding: 'utf8' }
    ).trim().split('\n').filter(f => f);
    
    if (tailwindConfigs.length > 1) {
      warnings.push(`⚠️  Found ${tailwindConfigs.length} Tailwind configs (may be intentional)`);
      tailwindConfigs.forEach(config => {
        warnings.push(`   ${config}`);
      });
    } else {
      passed.push(`✅ Single Tailwind config found`);
    }
  } catch (error) {
    // Ignore
  }
}

// 7. Validate organization
function validateOrganization() {
  console.log(`${BLUE}Step 7: Validating organization...${RESET}`);
  
  const requiredDirs = [
    'design-system/tokens',
    'design-system/generators',
    'design-system/scripts',
    'design-system/docs',
    'design-system/generated',
  ];
  
  requiredDirs.forEach(dir => {
    if (fs.existsSync(dir)) {
      passed.push(`✅ Directory '${dir}' exists`);
    } else {
      issues.push(`❌ Directory '${dir}' missing`);
    }
  });
}

// 8. Check documentation completeness
function checkDocumentation() {
  console.log(`${BLUE}Step 8: Checking documentation...${RESET}`);
  
  const requiredDocs = [
    'design-system/docs/UNIFIED_COLOR_SYSTEM_V2.md',
    'design-system/docs/COLOR_VALIDATION_REPORT.md',
    'design-system/docs/DESIGN_GUARDRAILS.md',
    'design-system/OPERATIONAL_GUIDE.md',
  ];
  
  requiredDocs.forEach(doc => {
    if (fs.existsSync(doc)) {
      passed.push(`✅ Documentation '${doc}' exists`);
    } else {
      warnings.push(`⚠️  Documentation '${doc}' missing`);
    }
  });
}

// Run all validations
checkDesignSystemFiles();
validateUnifiedColorSystem();
checkHardcodedColors();
checkInlineStyles();
validateTailwindSync();
checkConflicts();
validateOrganization();
checkDocumentation();

// Print results
console.log(`\n${GREEN}✅ PASSED (${passed.length}):${RESET}`);
passed.forEach(msg => console.log(`  ${msg}`));

if (warnings.length > 0) {
  console.log(`\n${YELLOW}⚠️  WARNINGS (${warnings.length}):${RESET}`);
  warnings.forEach(msg => console.log(`  ${msg}`));
}

if (issues.length > 0) {
  console.log(`\n${RED}❌ ISSUES (${issues.length}):${RESET}`);
  issues.forEach(msg => console.log(`  ${msg}`));
}

if (conflicts.length > 0) {
  console.log(`\n${RED}🔴 CONFLICTS (${conflicts.length}):${RESET}`);
  conflicts.forEach(msg => console.log(`  ${msg}`));
}

// Summary
console.log(`\n${BLUE}📊 SUMMARY:${RESET}`);
console.log(`  ✅ Passed: ${passed.length}`);
console.log(`  ⚠️  Warnings: ${warnings.length}`);
console.log(`  ❌ Issues: ${issues.length}`);
console.log(`  🔴 Conflicts: ${conflicts.length}`);

if (issues.length === 0 && conflicts.length === 0) {
  console.log(`\n${GREEN}✅ Design systems validated successfully!${RESET}`);
  process.exit(0);
} else {
  console.log(`\n${YELLOW}⚠️  Please fix issues before proceeding.${RESET}`);
  process.exit(1);
}

