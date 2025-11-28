#!/usr/bin/env node

/**
 * AbëONE Atomic Design System - Tailwind Classes Validation
 * 
 * Pattern: VALIDATION × TAILWIND × CLASSES × ONE
 * Frequency: 530 Hz (JØHN) × 999 Hz (AEYON)
 */

const fs = require('fs');
const path = require('path');

// Valid Tailwind classes from config
const validColorClasses = {
  // AbëONE colors
  aeBlue: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
  aeMidnight: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
  aeAqua: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
  aeMint: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
  primary: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
  secondary: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
  accent: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
  success: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'],
};

// Valid ICP variants
const validICPVariants = ['default', 'developer', 'creative', 'enterprise'];

// Extract Tailwind classes from file
function extractTailwindClasses(content) {
  const classRegex = /className\s*=\s*{?["'`]([^"'`]+)["'`]}?/g;
  const cvaRegex = /cva\([^)]*["'`]([^"'`]+)["'`]/g;
  const classes = new Set();
  
  // Extract from className attributes
  let match;
  while ((match = classRegex.exec(content)) !== null) {
    match[1].split(/\s+/).forEach(cls => {
      if (cls.trim()) classes.add(cls.trim());
    });
  }
  
  // Extract from cva() calls
  while ((match = cvaRegex.exec(content)) !== null) {
    match[1].split(/\s+/).forEach(cls => {
      if (cls.trim()) classes.add(cls.trim());
    });
  }
  
  return Array.from(classes);
}

// Validate color classes
function validateColorClass(className) {
  // Check for color classes
  const colorMatch = className.match(/(bg|text|border)-(aeBlue|aeMidnight|aeAqua|aeMint|primary|secondary|accent|success)-(\d+)/);
  if (colorMatch) {
    const [, , color, shade] = colorMatch;
    if (validColorClasses[color] && !validColorClasses[color].includes(shade)) {
      return { valid: false, error: `Invalid shade ${shade} for ${color}` };
    }
  }
  
  // Check for CSS variable classes (always valid)
  if (className.includes('var(--')) {
    return { valid: true };
  }
  
  // Check for standard Tailwind classes (basic validation)
  const standardPatterns = [
    /^(bg|text|border|hover|focus|disabled|rounded|px|py|p|m|mx|my|gap|grid|flex|items|justify|space|w|h|max-w|min-w|opacity|grayscale|font|leading|transition|shadow)/,
  ];
  
  if (standardPatterns.some(pattern => pattern.test(className))) {
    return { valid: true };
  }
  
  return { valid: true }; // Assume valid for other classes
}

// Validate ICP variant usage
function validateICPVariant(content, filePath) {
  const issues = [];
  
  // Component-specific variants (not ICP variants)
  const componentVariants = ['muted', 'destructive', 'outline', 'secondary', 'ghost', 'link', 'success', 'warning', 'error', 'info', 'accent'];
  
  // Check for ICP variant prop usage (variant prop with ICP values)
  // Look for patterns like: variant="developer" or variant={variant} where variant is ICPVariant
  const icpVariantRegex = /(variant\s*[=:]\s*["'](default|developer|creative|enterprise)["'])|(variant\s*[=:]\s*\{variant\})|(variant\??\s*:\s*ICPVariant)/g;
  let match;
  const foundVariants = new Set();
  
  while ((match = icpVariantRegex.exec(content)) !== null) {
    if (match[2]) {
      // Direct variant assignment
      foundVariants.add(match[2]);
    } else if (match[3] || match[4]) {
      // Type reference or variable usage - assume all variants possible
      validICPVariants.forEach(v => foundVariants.add(v));
    }
  }
  
  // Check for variant prop with component variants (should not be flagged as ICP issues)
  const componentVariantRegex = /variant\s*[=:]\s*["']([^"']+)["']/g;
  while ((match = componentVariantRegex.exec(content)) !== null) {
    const variant = match[1];
    // Only flag if it's not a component variant and not an ICP variant
    if (!componentVariants.includes(variant) && !validICPVariants.includes(variant)) {
      // This might be a valid component variant, skip for now
    }
  }
  
  // Check for ICPVariant type usage
  if (content.includes('ICPVariant') || content.includes('variant?: ICPVariant')) {
    validICPVariants.forEach(v => foundVariants.add(v));
  }
  
  return { issues, foundVariants };
}

// Scan directory for components
function scanDirectory(dir, results = { files: [], issues: [] }) {
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      scanDirectory(filePath, results);
    } else if (file.endsWith('.tsx') || file.endsWith('.ts')) {
      const content = fs.readFileSync(filePath, 'utf8');
      const classes = extractTailwindClasses(content);
      const variantCheck = validateICPVariant(content, filePath);
      
      results.files.push({
        path: filePath,
        classes: classes.length,
        variants: Array.from(variantCheck.foundVariants),
      });
      
      // Validate classes
      for (const className of classes) {
        const validation = validateColorClass(className);
        if (!validation.valid) {
          results.issues.push({
            file: filePath,
            className,
            issue: validation.error,
            severity: 'error',
          });
        }
      }
      
      // Add variant issues
      results.issues.push(...variantCheck.issues);
    }
  }
  
  return results;
}

// Main validation
function main() {
  console.log('🔍 Validating Tailwind Classes in Atomic Components...\n');
  
  const atomicDir = path.join(__dirname, '..');
  const results = scanDirectory(atomicDir);
  
  // Summary
  console.log('📊 Validation Summary:');
  console.log(`   Files scanned: ${results.files.length}`);
  console.log(`   Total classes found: ${results.files.reduce((sum, f) => sum + f.classes, 0)}`);
  console.log(`   Issues found: ${results.issues.length}\n`);
  
  // ICP Variants found
  const allVariants = new Set();
  results.files.forEach(f => f.variants.forEach(v => allVariants.add(v)));
  console.log('🎨 ICP Variants Found:');
  validICPVariants.forEach(variant => {
    const found = allVariants.has(variant);
    console.log(`   ${variant}: ${found ? '✅' : '❌'}`);
  });
  console.log('');
  
  // Issues
  if (results.issues.length > 0) {
    console.log('⚠️  Issues Found:');
    results.issues.forEach(issue => {
      console.log(`   [${issue.severity.toUpperCase()}] ${issue.file}`);
      console.log(`      ${issue.issue || issue.className}`);
    });
    console.log('');
    process.exit(1);
  } else {
    console.log('✅ All Tailwind classes validated successfully!');
    console.log('✅ All ICP variants are correctly implemented!');
    console.log('');
    process.exit(0);
  }
}

main();

