#!/usr/bin/env node
/**
 * Webinar System Setup Validator
 * 
 * Pattern: VALIDATION × SETUP × SEAMLESS × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Validates everything needed for webinar system to work.
 * NO RABBIT HOLES - Clear errors, clear fixes.
 */

const fs = require('fs')
const path = require('path')
const { execSync } = require('child_process')

const PROJECT_ROOT = process.cwd()
const WEBINARS_DIR = path.join(PROJECT_ROOT, 'webinars')
const ORCHESTRATOR = path.join(PROJECT_ROOT, 'scripts', 'webinar', 'master_orchestrator.py')
const DB_PATH = path.join(WEBINARS_DIR, 'webinars.db')

const checks = {
  python: false,
  orchestrator: false,
  database: false,
  dependencies: false,
  api: false,
  webinarsDir: false
}

const errors = []
const warnings = []

console.log('🔍 WEBINAR SYSTEM VALIDATION')
console.log('=' .repeat(60))
console.log()

// Check Python 3
console.log('✓ Checking Python 3...')
try {
  const pythonVersion = execSync('python3 --version', { encoding: 'utf-8' }).trim()
  console.log(`  ✅ ${pythonVersion}`)
  checks.python = true
} catch (error) {
  console.log('  ❌ Python 3 not found')
  errors.push('Python 3 is required. Install: brew install python3')
  checks.python = false
}

// Check orchestrator script
console.log('\n✓ Checking orchestrator script...')
if (fs.existsSync(ORCHESTRATOR)) {
  console.log(`  ✅ Found: ${ORCHESTRATOR}`)
  checks.orchestrator = true
} else {
  console.log(`  ❌ Not found: ${ORCHESTRATOR}`)
  errors.push(`Orchestrator script missing: ${ORCHESTRATOR}`)
  checks.orchestrator = false
}

// Check Python dependencies
console.log('\n✓ Checking Python dependencies...')
if (checks.python) {
  const requiredPackages = [
    'sqlite3',
    'json',
    'schedule',
    'openai',
    'dotenv'
  ]
  
  const missing = []
  for (const pkg of requiredPackages) {
    try {
      if (pkg === 'dotenv') {
        execSync('python3 -c "from dotenv import load_dotenv"', { 
          encoding: 'utf-8',
          stdio: 'pipe'
        })
      } else {
        execSync(`python3 -c "import ${pkg}"`, { 
          encoding: 'utf-8',
          stdio: 'pipe'
        })
      }
    } catch (error) {
      missing.push(pkg)
    }
  }
  
  if (missing.length === 0) {
    console.log('  ✅ All required Python packages available')
    checks.dependencies = true
  } else {
    console.log(`  ❌ Missing packages: ${missing.join(', ')}`)
    errors.push(`Install missing packages: pip3 install ${missing.map(p => p === 'dotenv' ? 'python-dotenv' : p).join(' ')}`)
    checks.dependencies = false
  }
}

// Check webinars directory
console.log('\n✓ Checking webinars directory...')
try {
  if (!fs.existsSync(WEBINARS_DIR)) {
    fs.mkdirSync(WEBINARS_DIR, { recursive: true })
    console.log(`  ✅ Created: ${WEBINARS_DIR}`)
  } else {
    console.log(`  ✅ Exists: ${WEBINARS_DIR}`)
  }
  checks.webinarsDir = true
} catch (error) {
  console.log(`  ❌ Cannot create: ${WEBINARS_DIR}`)
  errors.push(`Cannot create webinars directory: ${error.message}`)
  checks.webinarsDir = false
}

// Check database (will be created on first use)
console.log('\n✓ Checking database...')
if (fs.existsSync(DB_PATH)) {
  console.log(`  ✅ Database exists: ${DB_PATH}`)
  checks.database = true
} else {
  console.log(`  ⚠️  Database will be created on first use`)
  checks.database = true // Will be created automatically
}

// Check API routes
console.log('\n✓ Checking API routes...')
const apiRoutes = [
  path.join(PROJECT_ROOT, 'apps', 'web', 'app', 'api', 'webinar', 'register', 'route.ts'),
  path.join(PROJECT_ROOT, 'apps', 'web', 'app', 'api', 'webinar', 'list', 'route.ts'),
  path.join(PROJECT_ROOT, 'apps', 'web', 'app', 'api', 'webinar', '[id]', 'route.ts')
]

let apiRoutesExist = true
for (const route of apiRoutes) {
  if (!fs.existsSync(route)) {
    apiRoutesExist = false
    errors.push(`API route missing: ${route}`)
  }
}

if (apiRoutesExist) {
  console.log('  ✅ All API routes exist')
  checks.api = true
} else {
  console.log('  ❌ Some API routes missing')
  checks.api = false
}

// Summary
console.log('\n' + '='.repeat(60))
console.log('📊 VALIDATION SUMMARY')
console.log('='.repeat(60))

const allChecks = Object.values(checks)
const allPassed = allChecks.every(check => check === true)

if (allPassed) {
  console.log('\n✅ ALL CHECKS PASSED!')
  console.log('\n🚀 System is ready to use!')
  console.log('\nQuick Start:')
  console.log('  1. Create a webinar:')
  console.log('     python3 scripts/webinar/master_orchestrator.py --create --topic "My Webinar"')
  console.log('  2. Start frontend:')
  console.log('     cd apps/web && npm run dev')
  console.log('  3. Test registration:')
  console.log('     POST http://localhost:3000/api/webinar/register')
} else {
  console.log('\n❌ VALIDATION FAILED')
  
  if (errors.length > 0) {
    console.log('\n🔴 ERRORS (must fix):')
    errors.forEach((error, i) => {
      console.log(`  ${i + 1}. ${error}`)
    })
  }
  
  if (warnings.length > 0) {
    console.log('\n🟡 WARNINGS (recommended):')
    warnings.forEach((warning, i) => {
      console.log(`  ${i + 1}. ${warning}`)
    })
  }
  
  console.log('\n💡 Fix errors above, then run this script again.')
}

console.log('\n' + '='.repeat(60))

process.exit(allPassed ? 0 : 1)

