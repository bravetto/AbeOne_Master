import { NextRequest, NextResponse } from 'next/server'
export const dynamic = 'force-dynamic'
import { exec } from 'child_process'
import { promisify } from 'util'
import { join } from 'path'
import { existsSync } from 'fs'
import { withPublicApi } from '@/lib/middleware/api-wrapper'

const execAsync = promisify(exec)

/**
 * Webinar Test API Route
 * 
 * Pattern: TEST × WEBINAR × VALIDATION × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Quick test endpoint to verify everything works.
 * NO RABBIT HOLES - Clear status, clear errors.
 */

const PROJECT_ROOT = process.cwd()
const ORCHESTRATOR = join(PROJECT_ROOT, 'scripts', 'webinar', 'master_orchestrator.py')
const WEBINARS_DIR = join(PROJECT_ROOT, 'webinars')

interface TestResult {
  name: string
  status: 'pass' | 'fail' | 'warning'
  message: string
  details?: any
}

/**
 * GET /api/webinar/test
 * 
 * Runs comprehensive system test.
 */
export const GET = withPublicApi(async () => {
  const results: TestResult[] = []

  // Test 1: Python available
  try {
    await execAsync('python3 --version', { timeout: 5000 })
    results.push({
      name: 'Python 3',
      status: 'pass',
      message: 'Python 3 is available'
    })
  } catch (error) {
    results.push({
      name: 'Python 3',
      status: 'fail',
      message: 'Python 3 not found',
      details: 'Install: brew install python3'
    })
  }

  // Test 2: Orchestrator script exists
  if (existsSync(ORCHESTRATOR)) {
    results.push({
      name: 'Orchestrator Script',
      status: 'pass',
      message: 'Orchestrator script found'
    })
  } else {
    results.push({
      name: 'Orchestrator Script',
      status: 'fail',
      message: `Orchestrator script not found: ${ORCHESTRATOR}`
    })
  }

  // Test 3: Webinars directory exists
  if (existsSync(WEBINARS_DIR)) {
    results.push({
      name: 'Webinars Directory',
      status: 'pass',
      message: 'Webinars directory exists'
    })
  } else {
    results.push({
      name: 'Webinars Directory',
      status: 'warning',
      message: 'Webinars directory will be created on first use'
    })
  }

  // Test 4: Can run orchestrator (dry run)
  try {
    const { stdout } = await execAsync(
      `python3 "${ORCHESTRATOR}" --help`,
      { timeout: 10000, cwd: PROJECT_ROOT }
    )
    results.push({
      name: 'Orchestrator Execution',
      status: 'pass',
      message: 'Orchestrator script is executable'
    })
  } catch (error: any) {
    results.push({
      name: 'Orchestrator Execution',
      status: 'fail',
      message: 'Cannot execute orchestrator script',
      details: error.message
    })
  }

  // Test 5: Python dependencies
  try {
    await execAsync('python3 -c "import sqlite3; import json; import schedule"', {
      timeout: 5000
    })
    results.push({
      name: 'Python Dependencies',
      status: 'pass',
      message: 'All required Python packages available'
    })
  } catch (error) {
    results.push({
      name: 'Python Dependencies',
      status: 'fail',
      message: 'Missing Python packages',
      details: 'Install: pip3 install python-dotenv schedule'
    })
  }

  // Calculate summary
  const passed = results.filter(r => r.status === 'pass').length
  const failed = results.filter(r => r.status === 'fail').length
  const warnings = results.filter(r => r.status === 'warning').length
  const allPassed = failed === 0

  return NextResponse.json(
    {
      success: allPassed,
      summary: {
        total: results.length,
        passed,
        failed,
        warnings
      },
      results,
      ready: allPassed,
      message: allPassed
        ? '✅ All tests passed! System is ready.'
        : `❌ ${failed} test(s) failed. Check details above.`,
      nextSteps: allPassed
        ? [
            'Create a webinar: python3 scripts/webinar/master_orchestrator.py --create --topic "Test"',
            'Register: POST /api/webinar/register',
            'List: GET /api/webinar/list'
          ]
        : [
            'Fix the failed tests above',
            'Run validation: node scripts/webinar/validate_setup.js',
            'Then test again: GET /api/webinar/test'
          ],
      timestamp: new Date().toISOString()
    },
    {
      status: allPassed ? 200 : 503,
      headers: {
        'Cache-Control': 'no-store, must-revalidate'
      }
    }
  )
})

