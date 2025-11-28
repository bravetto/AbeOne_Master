#!/usr/bin/env node

/**
 * Categorize and organize root markdown files
 * Analyzes files and suggests organization structure
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const DOCS_DIR = path.join(ROOT_DIR, 'docs');

// Patterns for categorization
const PATTERNS = {
  status: [
    /_COMPLETE\.md$/i,
    /_STATUS\.md$/i,
    /_VALIDATION.*\.md$/i,
    /_EXECUTION.*\.md$/i,
    /_REPORT\.md$/i,
    /^AEYON_.*\.md$/i,
    /^ATOMIC_.*\.md$/i,
    /^ABEKEYS_.*\.md$/i,
    /^ABEVISION.*\.md$/i,
    /^AUTOMATION.*\.md$/i,
    /^CONVERGENCE.*\.md$/i,
    /^PHASE_.*\.md$/i,
  ],
  guides: [
    /_GUIDE\.md$/i,
    /_QUICK_START\.md$/i,
    /_USAGE.*\.md$/i,
    /^FIND_.*\.md$/i,
    /^QUICK_.*\.md$/i,
    /^SETUP.*\.md$/i,
    /^LOCALHOST.*\.md$/i,
  ],
  architecture: [
    /_ARCHITECTURE\.md$/i,
    /_DESIGN\.md$/i,
    /_STRUCTURE\.md$/i,
    /_PATTERN.*\.md$/i,
    /^PROJECT_.*\.md$/i,
    /^FOLDER_.*\.md$/i,
  ],
};

// Category subdirectories
const CATEGORIES = {
  status: {
    'design-system': /DESIGN|COLOR|PALETTE|TOKEN/i,
    integrations: /INTEGRATION|CONVERGENCE|ABEKEYS|ABEVISION/i,
    deployments: /DEPLOY|DEPLOYMENT|INFRASTRUCTURE/i,
  },
  guides: {
    'design-system': /DESIGN|COLOR|PALETTE|TOKEN|ADS/i,
    development: /DEV|SETUP|QUICK_START|LOCALHOST/i,
    deployment: /DEPLOY|DEPLOYMENT|CLOUDFLARE|VERCEL/i,
  },
  architecture: {
    'design-system': /DESIGN|COLOR|PALETTE|TOKEN|ADS/i,
    apps: /APP|WEB|FRONTEND|NEXT/i,
    integrations: /INTEGRATION|CONVERGENCE/i,
  },
};

function categorizeFile(filename) {
  // Skip if already in docs/ or other directories
  if (filename.includes('/') || filename.startsWith('.')) {
    return null;
  }

  // Determine main category
  let mainCategory = null;
  for (const [category, patterns] of Object.entries(PATTERNS)) {
    if (patterns.some(pattern => pattern.test(filename))) {
      mainCategory = category;
      break;
    }
  }

  if (!mainCategory) {
    return null; // Unknown category
  }

  // Determine subcategory
  let subcategory = null;
  const subcategories = CATEGORIES[mainCategory];
  for (const [subcat, pattern] of Object.entries(subcategories)) {
    if (pattern.test(filename)) {
      subcategory = subcat;
      break;
    }
  }

  // Default subcategory
  if (!subcategory) {
    subcategory = mainCategory === 'status' ? 'general' : 'general';
  }

  return {
    mainCategory,
    subcategory,
    targetPath: `docs/${mainCategory}/${subcategory}/${filename}`,
  };
}

function analyzeFiles() {
  const files = fs.readdirSync(ROOT_DIR);
  const markdownFiles = files.filter(f => f.endsWith('.md') && !f.includes('/'));

  const categorized = {
    status: {},
    guides: {},
    architecture: {},
    unknown: [],
  };

  markdownFiles.forEach(file => {
    const category = categorizeFile(file);
    if (category) {
      if (!categorized[category.mainCategory][category.subcategory]) {
        categorized[category.mainCategory][category.subcategory] = [];
      }
      categorized[category.mainCategory][category.subcategory].push({
        file,
        targetPath: category.targetPath,
      });
    } else {
      categorized.unknown.push(file);
    }
  });

  return categorized;
}

function generateReport(categorized) {
  console.log('\n DOCUMENTATION CATEGORIZATION REPORT\n');
  console.log('=' .repeat(60));

  let total = 0;

  Object.entries(categorized).forEach(([category, subcats]) => {
    if (category === 'unknown') return;

    const categoryTotal = Object.values(subcats).reduce((sum, files) => sum + files.length, 0);
    total += categoryTotal;

    if (categoryTotal > 0) {
      console.log(`\n ${category.toUpperCase()} (${categoryTotal} files)`);
      Object.entries(subcats).forEach(([subcat, files]) => {
        if (files.length > 0) {
          console.log(`   ${subcat}/ (${files.length} files)`);
          files.slice(0, 5).forEach(({ file }) => {
            console.log(`     • ${file}`);
          });
          if (files.length > 5) {
            console.log(`     ... and ${files.length - 5} more`);
          }
        }
      });
    }
  });

  if (categorized.unknown.length > 0) {
    console.log(`\n UNCATEGORIZED (${categorized.unknown.length} files)`);
    categorized.unknown.slice(0, 10).forEach(file => {
      console.log(`   • ${file}`);
    });
    if (categorized.unknown.length > 10) {
      console.log(`   ... and ${categorized.unknown.length - 10} more`);
    }
  }

  console.log(`\n${'='.repeat(60)}`);
  console.log(`\n Total categorized: ${total}`);
  console.log(` Unclassified: ${categorized.unknown.length}`);
  console.log(` Total markdown files: ${total + categorized.unknown.length}\n`);
}

function generateMoveScript(categorized) {
  const moves = [];

  Object.entries(categorized).forEach(([category, subcats]) => {
    if (category === 'unknown') return;

    Object.entries(subcats).forEach(([subcat, files]) => {
      files.forEach(({ file, targetPath }) => {
        moves.push({
          from: path.join(ROOT_DIR, file),
          to: path.join(ROOT_DIR, targetPath),
          file,
        });
      });
    });
  });

  const script = `#!/bin/bash
# Auto-generated file organization script
# Generated: ${new Date().toISOString()}

set -e

echo " Organizing documentation files..."
echo ""

# Create directories
${[...new Set(moves.map(m => path.dirname(m.to)))].map(dir => `mkdir -p "${dir}"`).join('\n')}

# Move files
${moves.map(m => `mv "${m.from}" "${m.to}" && echo " Moved: ${m.file}"`).join('\n')}

echo ""
echo " Organization complete!"
`;

  fs.writeFileSync(
    path.join(ROOT_DIR, 'scripts/organize-docs.sh'),
    script,
    { mode: 0o755 }
  );

  console.log(' Generated organization script: scripts/organize-docs.sh');
  console.log('   Run: ./scripts/organize-docs.sh to execute\n');
}

// Main execution
console.log(' Analyzing root markdown files...\n');

const categorized = analyzeFiles();
generateReport(categorized);
generateMoveScript(categorized);

// Save analysis to JSON
fs.writeFileSync(
  path.join(ROOT_DIR, 'docs/categorization-analysis.json'),
  JSON.stringify(categorized, null, 2)
);

console.log(' Analysis saved to: docs/categorization-analysis.json');

