#!/usr/bin/env node

/**
 * Validate file organization against rules
 * Checks naming conventions, file locations, and structure
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const DOCS_DIR = path.join(ROOT_DIR, 'docs');

// Rules
const RULES = {
  rootMarkdownFiles: {
    maxAllowed: 10, // Only essential files
    allowed: ['README.md', 'LICENSE.md', 'CHANGELOG.md'],
  },
  namingConventions: {
    status: /^[A-Z_]+_(COMPLETE|STATUS|VALIDATION|EXECUTION|REPORT)\.md$/i,
    guides: /^[A-Z_]+_(GUIDE|QUICK_START|USAGE)\.md$/i,
    architecture: /^[A-Z_]+_(ARCHITECTURE|DESIGN|STRUCTURE|PATTERN)\.md$/i,
  },
  requiredDocs: {
    'docs/INDEX.md': 'Master navigation index',
    'docs/APPLICATION_DEFINITIONS.md': 'Application definitions',
    'docs/ORGANIZATION_RULES.md': 'Organization rules',
    'design-system/README.md': 'Design system entry point',
    'apps/web/README.md': 'Frontend entry point',
  },
};

function checkRootMarkdownFiles() {
  const files = fs.readdirSync(ROOT_DIR);
  const markdownFiles = files.filter(f => f.endsWith('.md') && !f.includes('/'));

  const violations = [];
  const allowed = RULES.rootMarkdownFiles.allowed.map(f => f.toLowerCase());

  markdownFiles.forEach(file => {
    if (!allowed.includes(file.toLowerCase())) {
      violations.push(file);
    }
  });

  return {
    total: markdownFiles.length,
    violations,
    maxAllowed: RULES.rootMarkdownFiles.maxAllowed,
    passed: violations.length === 0 && markdownFiles.length <= RULES.rootMarkdownFiles.maxAllowed,
  };
}

function checkNamingConventions() {
  const violations = [];

  function checkDirectory(dir, category) {
    if (!fs.existsSync(dir)) return;

    const files = fs.readdirSync(dir, { withFileTypes: true });
    files.forEach(file => {
      if (file.isFile() && file.name.endsWith('.md')) {
        const pattern = RULES.namingConventions[category];
        if (pattern && !pattern.test(file.name)) {
          violations.push({
            file: path.join(dir, file.name),
            category,
            issue: 'Naming convention violation',
          });
        }
      } else if (file.isDirectory()) {
        checkDirectory(path.join(dir, file.name), category);
      }
    });
  }

  ['status', 'guides', 'architecture'].forEach(category => {
    const categoryDir = path.join(DOCS_DIR, category);
    if (fs.existsSync(categoryDir)) {
      checkDirectory(categoryDir, category);
    }
  });

  return {
    violations,
    passed: violations.length === 0,
  };
}

function checkRequiredDocs() {
  const missing = [];

  Object.entries(RULES.requiredDocs).forEach(([file, description]) => {
    const filePath = path.join(ROOT_DIR, file);
    if (!fs.existsSync(filePath)) {
      missing.push({ file, description });
    }
  });

  return {
    missing,
    passed: missing.length === 0,
  };
}

function checkDirectoryStructure() {
  const requiredDirs = [
    'docs',
    'docs/status',
    'docs/guides',
    'docs/architecture',
    'design-system',
    'design-system/tokens',
    'design-system/docs',
    'apps',
    'apps/web',
  ];

  const missing = [];

  requiredDirs.forEach(dir => {
    const dirPath = path.join(ROOT_DIR, dir);
    if (!fs.existsSync(dirPath)) {
      missing.push(dir);
    }
  });

  return {
    missing,
    passed: missing.length === 0,
  };
}

function runValidation() {
  console.log('\n🔍 VALIDATING ORGANIZATION\n');
  console.log('='.repeat(60));

  const results = {
    rootFiles: checkRootMarkdownFiles(),
    naming: checkNamingConventions(),
    requiredDocs: checkRequiredDocs(),
    structure: checkDirectoryStructure(),
  };

  // Report results
  console.log('\n📁 Root Markdown Files:');
  if (results.rootFiles.passed) {
    console.log('   ✅ PASSED');
  } else {
    console.log(`   ❌ FAILED (${results.rootFiles.violations.length} violations)`);
    console.log(`   Found ${results.rootFiles.total} markdown files in root`);
    console.log(`   Max allowed: ${results.rootFiles.maxAllowed}`);
    if (results.rootFiles.violations.length > 0) {
      console.log('   Violations:');
      results.rootFiles.violations.slice(0, 10).forEach(file => {
        console.log(`     • ${file}`);
      });
      if (results.rootFiles.violations.length > 10) {
        console.log(`     ... and ${results.rootFiles.violations.length - 10} more`);
      }
    }
  }

  console.log('\n📝 Naming Conventions:');
  if (results.naming.passed) {
    console.log('   ✅ PASSED');
  } else {
    console.log(`   ❌ FAILED (${results.naming.violations.length} violations)`);
    results.naming.violations.slice(0, 5).forEach(({ file, issue }) => {
      console.log(`     • ${file}: ${issue}`);
    });
  }

  console.log('\n📚 Required Documentation:');
  if (results.requiredDocs.passed) {
    console.log('   ✅ PASSED');
  } else {
    console.log(`   ❌ FAILED (${results.requiredDocs.missing.length} missing)`);
    results.requiredDocs.missing.forEach(({ file, description }) => {
      console.log(`     • ${file}: ${description}`);
    });
  }

  console.log('\n🏗️  Directory Structure:');
  if (results.structure.passed) {
    console.log('   ✅ PASSED');
  } else {
    console.log(`   ❌ FAILED (${results.structure.missing.length} missing)`);
    results.structure.missing.forEach(dir => {
      console.log(`     • ${dir}/`);
    });
  }

  // Summary
  const allPassed = Object.values(results).every(r => r.passed);

  console.log('\n' + '='.repeat(60));
  if (allPassed) {
    console.log('\n✅ ALL VALIDATIONS PASSED\n');
    process.exit(0);
  } else {
    console.log('\n❌ SOME VALIDATIONS FAILED\n');
    process.exit(1);
  }
}

runValidation();

