#!/usr/bin/env node
/**
 * Design Drift Prevention Script
 * Scans codebase for design drift violations
 * 
 * Usage: node design-system/scripts/prevent-drift.js [--fix]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const violations = [];
const fixable = [];

// Forbidden patterns
const FORBIDDEN_PATTERNS = [
  {
    name: 'Hardcoded Purple',
    pattern: /bg-purple|text-purple|purple-\d+/g,
    message: 'Use design tokens (lux/primary) instead of hardcoded purple',
    fix: (match) => match.replace(/purple/g, 'lux').replace(/bg-purple/g, 'bg-lux').replace(/text-purple/g, 'text-lux'),
  },
  {
    name: 'Hardcoded Gray',
    pattern: /text-gray-\d+|bg-gray-\d+|border-gray-\d+/g,
    message: 'Use design tokens (neutral) instead of hardcoded gray',
    fix: (match) => match.replace(/gray/g, 'neutral'),
  },
  {
    name: 'Hardcoded Hex Colors',
    pattern: /#[0-9a-fA-F]{6}/g,
    message: 'Use design tokens instead of hex colors',
    fix: null, // Manual fix required
  },
  {
    name: 'Inline Styles',
    pattern: /style=\{[^}]*color|style=\{[^}]*background|style=\{[^}]*padding|style=\{[^}]*margin/g,
    message: 'Use Tailwind classes instead of inline styles',
    fix: null, // Manual fix required
  },
];

// Allowed files (skip these)
const ALLOWED_FILES = [
  'node_modules',
  '.next',
  'design-system/tokens',
  'design-system/generated',
  'tailwind.config.js', // Generated file
];

function scanFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const relativePath = path.relative(process.cwd(), filePath);
    
    FORBIDDEN_PATTERNS.forEach(({ name, pattern, message, fix }) => {
      const matches = content.match(pattern);
      if (matches) {
        matches.forEach(match => {
          violations.push({
            file: relativePath,
            pattern: name,
            match,
            message,
            fixable: fix !== null,
            fix,
          });
        });
      }
    });
  } catch (error) {
    // Skip files that can't be read
  }
}

function scanDirectory(dir) {
  const files = fs.readdirSync(dir, { withFileTypes: true });
  
  files.forEach(file => {
    const fullPath = path.join(dir, file.name);
    const relativePath = path.relative(process.cwd(), fullPath);
    
    // Skip allowed files/dirs
    if (ALLOWED_FILES.some(allowed => relativePath.includes(allowed))) {
      return;
    }
    
    if (file.isDirectory()) {
      scanDirectory(fullPath);
    } else if (file.isFile() && /\.(tsx?|jsx?|css)$/.test(file.name)) {
      scanFile(fullPath);
    }
  });
}

// Scan apps/web directory
console.log('🔍 Scanning for design drift violations...\n');

const scanDirs = ['apps/web/app', 'apps/web/components'];
scanDirs.forEach(dir => {
  if (fs.existsSync(dir)) {
    scanDirectory(dir);
  }
});

// Group violations by file
const violationsByFile = {};
violations.forEach(v => {
  if (!violationsByFile[v.file]) {
    violationsByFile[v.file] = [];
  }
  violationsByFile[v.file].push(v);
});

// Print results
if (violations.length === 0) {
  console.log('✅ No design drift violations found!\n');
  process.exit(0);
}

console.log(`❌ Found ${violations.length} design drift violations:\n`);

Object.keys(violationsByFile).forEach(file => {
  console.log(`📄 ${file}:`);
  violationsByFile[file].forEach(v => {
    console.log(`   ${v.pattern}: ${v.match}`);
    console.log(`   → ${v.message}`);
    if (v.fixable) {
      console.log(`   💡 Fixable: ${v.fix(v.match)}`);
    }
    console.log('');
  });
});

console.log(`\n📊 Summary:`);
console.log(`   Total violations: ${violations.length}`);
console.log(`   Files affected: ${Object.keys(violationsByFile).length}`);
console.log(`   Fixable: ${violations.filter(v => v.fixable).length}`);

if (process.argv.includes('--fix')) {
  console.log('\n🔧 Fix mode not yet implemented. Please fix manually.');
}

process.exit(1);

