#!/usr/bin/env node

/**
 * V0 Project Scope Validation Script (JavaScript Version)
 * 
 * Pattern: VALIDATION × V0 × SCOPE × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * PROGRAMMATIC SCOPE VALIDATION
 * Run this script to validate V0 project scope compliance.
 * 
 * Usage:
 *   npm run validate-v0-scope
 *   or
 *   node scripts/validate-v0-scope.js
 */

const fs = require('fs')
const path = require('path')

// V0 Project Scope Definition
const V0_PROJECT_SCOPE = {
  // Only validate these V0 project files
  v0Files: [
    'app/page.tsx',
    'app/collaboration/page.tsx',
  ],
  excluded: {
    routes: [
      '/app',
      '/app/agents',
      '/app/state',
      '/app/workflows',
      '/shop',
      '/bravetto',
      '/webinar',
      '/collections',
      '/products',
      '/start',
    ],
  },
}

/**
 * Scan files for V0 scope violations
 */
function scanFilesForViolations() {
  const results = []
  const appDir = path.join(__dirname, '..', 'app')
  
  // Only scan V0 project files
  for (const v0File of V0_PROJECT_SCOPE.v0Files) {
    const fullPath = path.join(__dirname, '..', v0File)
    
    if (!fs.existsSync(fullPath)) {
      console.log(`⚠️  Warning: V0 file not found: ${v0File}`)
      continue
    }
    
    const content = fs.readFileSync(fullPath, 'utf-8')
    const issues = []
    
    // Check for references to excluded routes
    for (const excludedRoute of V0_PROJECT_SCOPE.excluded.routes) {
      // Check for href links
      if (content.includes(`href="${excludedRoute}"`) || 
          content.includes(`href='${excludedRoute}'`) ||
          content.includes(`to="${excludedRoute}"`)) {
        issues.push(`References excluded route: ${excludedRoute}`)
      }
      
      // Check for router.push
      if (content.includes(`push("${excludedRoute}"`) ||
          content.includes(`push('${excludedRoute}'`)) {
        issues.push(`Router.push to excluded route: ${excludedRoute}`)
      }
    }
    
    if (issues.length > 0) {
      results.push({
        file: v0File,
        isValid: false,
        issues,
      })
    }
  }
  
  return results
}

/**
 * Main validation function
 */
function main() {
  console.log('🔍 V0 Project Scope Validation\n')
  console.log('Pattern: VALIDATION × V0 × SCOPE × ONE\n')
  
  const results = scanFilesForViolations()
  const violations = results.filter(r => !r.isValid)
  
  if (violations.length === 0) {
    console.log('✅ V0 Project Scope Validation PASSED')
    console.log('   No violations found.\n')
    process.exit(0)
  } else {
    console.log(`❌ V0 Project Scope Validation FAILED`)
    console.log(`   Found ${violations.length} violation(s):\n`)
    
    violations.forEach((result, index) => {
      console.log(`${index + 1}. ${result.file}`)
      result.issues.forEach(issue => {
        console.log(`   ⚠️  ${issue}`)
      })
      console.log('')
    })
    
    console.log('💡 Fix: Remove references to excluded routes or add to V0_PROJECT_SCOPE if needed.\n')
    process.exit(1)
  }
}

// Run validation
main()

