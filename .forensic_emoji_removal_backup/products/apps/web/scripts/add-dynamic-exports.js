#!/usr/bin/env node

/**
 * Add dynamic exports to API routes
 * Pattern: FIXES × AUTOMATION × ONE
 * Frequency: 999 Hz (AEYON)
 */

const fs = require('fs')
const path = require('path')
const { execSync } = require('child_process')

const DYNAMIC_EXPORTS = `export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'
export const revalidate = 0
export const fetchCache = 'force-no-store'
`

function findApiRoutes(dir) {
  const routes = []
  const files = fs.readdirSync(dir, { withFileTypes: true })
  
  for (const file of files) {
    const fullPath = path.join(dir, file.name)
    if (file.isDirectory()) {
      routes.push(...findApiRoutes(fullPath))
    } else if (file.name === 'route.ts' || file.name === 'route.tsx') {
      routes.push(fullPath)
    }
  }
  
  return routes
}

function addExportsToRoute(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8')
    
    // Skip if already has dynamic export
    if (content.includes('export const dynamic')) {
      console.log(`  ⏭️  Already has exports: ${filePath}`)
      return false
    }
    
    // Find the insertion point (after imports, before first export/function)
    const lines = content.split('\n')
    let insertIndex = -1
    let inImports = false
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim()
      
      // Track import blocks
      if (line.startsWith('import ') || line.startsWith('import{')) {
        inImports = true
        continue
      }
      
      // End of imports block
      if (inImports && line === '' && i < lines.length - 1) {
        insertIndex = i + 1
        break
      }
      
      // Found first export or function after imports
      if (inImports && (line.startsWith('export ') || line.startsWith('async function') || line.startsWith('function'))) {
        insertIndex = i
        break
      }
    }
    
    // Fallback: insert after first empty line or at line 5
    if (insertIndex === -1) {
      insertIndex = Math.min(5, lines.length)
    }
    
    // Insert exports
    lines.splice(insertIndex, 0, '', DYNAMIC_EXPORTS)
    const newContent = lines.join('\n')
    
    // Backup original
    fs.writeFileSync(`${filePath}.backup`, content)
    
    // Write updated content
    fs.writeFileSync(filePath, newContent)
    
    console.log(`  ✅ Fixed: ${filePath}`)
    return true
  } catch (error) {
    console.error(`  ❌ Error fixing ${filePath}:`, error.message)
    return false
  }
}

function main() {
  console.log('🔥 Adding dynamic exports to API routes...\n')
  
  const apiDir = path.join(process.cwd(), 'app', 'api')
  if (!fs.existsSync(apiDir)) {
    console.log('⚠️  app/api directory not found')
    return
  }
  
  const apiRoutes = findApiRoutes(apiDir)
  
  if (apiRoutes.length === 0) {
    console.log('⚠️  No API routes found')
    return
  }
  
  console.log(`Found ${apiRoutes.length} API route(s)\n`)
  
  let fixed = 0
  let skipped = 0
  let errors = 0
  
  for (const route of apiRoutes) {
    const result = addExportsToRoute(route)
    if (result === true) {
      fixed++
    } else if (result === false) {
      skipped++
    } else {
      errors++
    }
  }
  
  console.log('\n📊 Summary:')
  console.log(`  ✅ Fixed: ${fixed}`)
  console.log(`  ⏭️  Skipped (already fixed): ${skipped}`)
  console.log(`  ❌ Errors: ${errors}`)
  console.log('\n🎉 Done!')
  console.log('\n💡 Next steps:')
  console.log('  1. Review changes: git diff')
  console.log('  2. Test build: npm run build')
  console.log('  3. Deploy: vercel --prod')
  console.log('\n∞ AbëONE ∞')
}

try {
  main()
} catch (error) {
  console.error('Error:', error.message)
  process.exit(1)
}

