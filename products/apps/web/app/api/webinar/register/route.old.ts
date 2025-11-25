import { NextRequest, NextResponse } from 'next/server'
import { exec } from 'child_process'
import { promisify } from 'util'
import { join } from 'path'
import { withPublicApi } from '@/lib/middleware/api-wrapper'

const execAsync = promisify(exec)

/**
 * Webinar Registration API Route
 * 
 * Pattern: API × WEBINAR × REGISTRATION × INTEGRATION × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Registers attendees for webinars using Python orchestrator.
 * Enterprise-grade: validated, error-handled, database-integrated.
 */

// SAFETY: Path resolution - works from any directory
const PROJECT_ROOT = process.cwd()
const PYTHON_ORCHESTRATOR = join(PROJECT_ROOT, 'scripts', 'webinar', 'master_orchestrator.py')
const PYTHON_TIMEOUT = 30000 // 30 seconds

/**
 * Call Python orchestrator to register attendee
 * 
 * SAFETY: Validates inputs, handles subprocess errors, timeout protection
 * ASSUMES: Python 3 available, orchestrator script exists
 */
async function registerViaOrchestrator(
  webinarId: string,
  email: string,
  name: string
): Promise<{ success: boolean; registrationId?: number; error?: string; output?: string }> {
  try {
    // VALIDATION: Check script exists
    const fs = await import('fs/promises')
    try {
      await fs.access(PYTHON_ORCHESTRATOR)
    } catch {
      return {
        success: false,
        error: `Orchestrator script not found: ${PYTHON_ORCHESTRATOR}`
      }
    }

    // SAFETY: Sanitize inputs (webinarId, email, name)
    const sanitizedWebinarId = webinarId.replace(/[^a-zA-Z0-9_-]/g, '')
    const sanitizedEmail = email.trim().toLowerCase()
    const sanitizedName = name.trim()

    // VALIDATION: Basic email format check
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(sanitizedEmail)) {
      return {
        success: false,
        error: 'Invalid email format'
      }
    }

    // Call Python orchestrator
    const command = `python3 "${PYTHON_ORCHESTRATOR}" --register --webinar-id "${sanitizedWebinarId}" --email "${sanitizedEmail}" --name "${sanitizedName}"`
    
    const { stdout, stderr } = await Promise.race([
      execAsync(command, {
        cwd: PROJECT_ROOT,
        timeout: PYTHON_TIMEOUT,
        maxBuffer: 10 * 1024 * 1024 // 10MB buffer
      }),
      new Promise<never>((_, reject) =>
        setTimeout(() => reject(new Error('Python script timeout')), PYTHON_TIMEOUT)
      )
    ]) as { stdout: string; stderr: string }

    // Parse output for registration ID
    const output = stdout + stderr
    const registrationMatch = output.match(/Registered in database: (\d+)/)
    const registrationId = registrationMatch ? parseInt(registrationMatch[1], 10) : undefined

    // Check for errors in output
    if (output.includes('❌') || output.includes('Error') || output.includes('not found')) {
      return {
        success: false,
        error: output.includes('not found') 
          ? `Webinar ${sanitizedWebinarId} not found`
          : 'Registration failed',
        output
      }
    }

    return {
      success: true,
      registrationId,
      output
    }
  } catch (error: any) {
    // VERIFY: Error handling
    if (error.code === 'ETIMEDOUT' || error.message.includes('timeout')) {
      return {
        success: false,
        error: 'Registration timeout - please try again'
      }
    }
    
    return {
      success: false,
      error: error.message || 'Registration failed',
      output: error.stdout || error.stderr || ''
    }
  }
}

/**
 * POST /api/webinar/register
 * 
 * Registers an attendee for a webinar.
 * 
 * Body: {
 *   webinarId: string (required)
 *   email: string (required, valid email)
 *   name: string (required)
 * }
 */
export const POST = withPublicApi(async (request: NextRequest) => {
  try {
    // VALIDATION: Parse and validate request body
    const body = await request.json()
    
    const { webinarId, email, name } = body

    // VALIDATION: Required fields
    if (!webinarId || !email || !name) {
      return NextResponse.json(
        {
          success: false,
          error: 'Missing required fields: webinarId, email, name'
        },
        { status: 400 }
      )
    }

    // VALIDATION: Type checks
    if (typeof webinarId !== 'string' || typeof email !== 'string' || typeof name !== 'string') {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid field types: all fields must be strings'
        },
        { status: 400 }
      )
    }

    // Register via Python orchestrator
    const result = await registerViaOrchestrator(webinarId, email, name)

    if (!result.success) {
      return NextResponse.json(
        {
          success: false,
          error: result.error || 'Registration failed',
          details: result.output
        },
        { status: 400 }
      )
    }

    // SUCCESS: Return registration confirmation
    return NextResponse.json(
      {
        success: true,
        message: 'Successfully registered for webinar',
        registrationId: result.registrationId,
        webinarId,
        email,
        name,
        timestamp: new Date().toISOString()
      },
      {
        status: 201,
        headers: {
          'Cache-Control': 'no-store, must-revalidate'
        }
      }
    )
  } catch (error: any) {
    // VERIFY: Error handling
    console.error('Webinar registration error:', error)

    // Handle JSON parse errors
    if (error instanceof SyntaxError || error.message?.includes('JSON')) {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid JSON in request body'
        },
        { status: 400 }
      )
    }

    return NextResponse.json(
      {
        success: false,
        error: error.message || 'Internal server error during registration'
      },
      { status: 500 }
    )
  }
})

/**
 * GET /api/webinar/register
 * 
 * Health check endpoint.
 */
export const GET = withPublicApi(async () => {
  return NextResponse.json(
    {
      success: true,
      message: 'Webinar registration API is operational',
      endpoints: {
        POST: '/api/webinar/register - Register attendee',
        GET: '/api/webinar/register - Health check'
      }
    },
    {
      headers: {
        'Cache-Control': 'no-store, must-revalidate'
      }
    }
  )
})

