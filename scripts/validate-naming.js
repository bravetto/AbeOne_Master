#!/usr/bin/env node

/**
 * Validate file naming conventions
 * Checks that files follow established naming patterns
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');

// Naming patterns
const PATTERNS = {
  status: {
    pattern: /^[A-Z_]+_(COMPLETE|STATUS|VALIDATION|EXECUTION|REPORT|SUMMARY)\.md$/i,
    examples: ['DESIGN_SYSTEM_COMPLETE.md', 'INTEGRATION_STATUS.md'],
  },
  guides: {
    pattern: /^[A-Z_]+_(GUIDE|QUICK_START|USAGE|SETUP)\.md$/i,
    examples: ['ADS_V1_USAGE_GUIDE.md', 'QUICK_START_GUIDE.md'],
  },
  architecture: {
    pattern: /^[A-Z_]+_(ARCHITECTURE|DESIGN|STRUCTURE|PATTERN)\.md$/i,
    examples: ['DESIGN_SYSTEM_ARCHITECTURE.md', 'APPS_STRUCTURE.md'],
  },
};

function validateFile(filePath, category) {
  const filename = path.basename(filePath);
  const pattern = PATTERNS[category]?.pattern;

  if (!pattern) {
    return { valid: true, reason: 'No pattern defined' };
  }

  const valid = pattern.test(filename);
  return {
    valid,
    filename,
    category,
    reason: valid ? 'Valid' : `Does not match ${category} pattern`,
    expected: PATTERNS[category].examples,
  };
}

function scanDirectory(dir, category, results = []) {
  if (!fs.existsSync(dir)) return results;

  const files = fs.readdirSync(dir, { withFileTypes: true });

  files.forEach(file => {
    const filePath = path.join(dir, file.name);

    if (file.isFile() && file.name.endsWith('.md')) {
      const validation = validateFile(filePath, category);
      if (!validation.valid) {
        results.push(validation);
      }
    } else if (file.isDirectory()) {
      scanDirectory(filePath, category, results);
    }
  });

  return results;
}

function runValidation() {
  console.log('\n VALIDATING NAMING CONVENTIONS\n');
  console.log('='.repeat(60));

  const violations = [];

  // Check docs/status
  const statusDir = path.join(ROOT_DIR, 'docs/status');
  violations.push(...scanDirectory(statusDir, 'status'));

  // Check docs/guides
  const guidesDir = path.join(ROOT_DIR, 'docs/guides');
  violations.push(...scanDirectory(guidesDir, 'guides'));

  // Check docs/architecture
  const archDir = path.join(ROOT_DIR, 'docs/architecture');
  violations.push(...scanDirectory(archDir, 'architecture'));

  // Report
  if (violations.length === 0) {
    console.log('\n ALL FILES FOLLOW NAMING CONVENTIONS\n');
    process.exit(0);
  } else {
    console.log(`\n FOUND ${violations.length} NAMING VIOLATIONS\n`);

    violations.forEach(({ filename, category, reason, expected }) => {
      console.log(`   ${filename}`);
      console.log(`   Category: ${category}`);
      console.log(`   Issue: ${reason}`);
      console.log(`   Expected pattern: ${PATTERNS[category].pattern}`);
      console.log(`   Examples: ${expected.join(', ')}`);
      console.log('');
    });

    console.log('='.repeat(60));
    process.exit(1);
  }
}

runValidation();

