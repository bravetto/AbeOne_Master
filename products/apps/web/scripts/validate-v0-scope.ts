#!/usr/bin/env ts-node

/**
 * V0 Project Scope Validation Script
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
 *   ts-node scripts/validate-v0-scope.ts
 */

import * as fs from 'fs'
import * as path from 'path'
import { V0_PROJECT_SCOPE, validateV0Scope, isExcludedRoute } from '../V0_PROJECT_SCOPE'

interface ValidationResult {
  file: string
  isValid: boolean
  issues: string[]
}

/**
 * Scan files for V0 scope violations
 */
function scanFilesForViolations(): ValidationResult[] {
  const results: ValidationResult[] = []
  const appDir = path.join(__dirname, '..', 'app')
  
  // Scan all route files
  function scanDirectory(dir: string, relativePath: string = '') {
    const entries = fs.readdirSync(dir, { withFileTypes: true })
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name)
      const relativeFilePath = path.join(relativePath, entry.name)
      
      if (entry.isDirectory()) {
        // Check if directory is excluded
        const routePath = '/' + relativeFilePath.replace(/\\/g, '/')
        if (isExcludedRoute(routePath)) {
          results.push({
            file: relativeFilePath,
            isValid: false,
            issues: [`Directory "${routePath}" is EXCLUDED from V0 project. Do not modify.`],
          })
        }
        scanDirectory(fullPath, relativeFilePath)
      } else if (entry.name.endsWith('.tsx') || entry.name.endsWith('.ts')) {
        // Check if file references excluded routes
        const content = fs.readFileSync(fullPath, 'utf-8')
        const issues: string[] = []
        
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
            file: relativeFilePath,
            isValid: false,
            issues,
          })
        }
      }
    }
  }
  
  scanDirectory(appDir, 'app')
  
  return results
}

/**
 * Main validation function
 */
function main() {
  console.log(' V0 Project Scope Validation\n')
  console.log('Pattern: VALIDATION × V0 × SCOPE × ONE\n')
  
  const results = scanFilesForViolations()
  const violations = results.filter(r => !r.isValid)
  
  if (violations.length === 0) {
    console.log(' V0 Project Scope Validation PASSED')
    console.log('   No violations found.\n')
    process.exit(0)
  } else {
    console.log(` V0 Project Scope Validation FAILED`)
    console.log(`   Found ${violations.length} violation(s):\n`)
    
    violations.forEach((result, index) => {
      console.log(`${index + 1}. ${result.file}`)
      result.issues.forEach(issue => {
        console.log(`     ${issue}`)
      })
      console.log('')
    })
    
    console.log(' Fix: Remove references to excluded routes or add to V0_PROJECT_SCOPE if needed.\n')
    process.exit(1)
  }
}

// Run validation
if (require.main === module) {
  main()
}

export { scanFilesForViolations }

