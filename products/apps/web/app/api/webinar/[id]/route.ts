import { NextRequest, NextResponse } from 'next/server'
export const dynamic = 'force-dynamic'
import { exec } from 'child_process'
import { promisify } from 'util'
import { join } from 'path'
import { readFile } from 'fs/promises'
import { existsSync } from 'fs'

const execAsync = promisify(exec)

/**
 * Webinar Detail API Route
 * 
 * Pattern: API × WEBINAR × DETAIL × INTEGRATION × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Gets detailed information about a specific webinar.
 */

const PROJECT_ROOT = process.cwd()
const WEBINARS_DIR = join(PROJECT_ROOT, 'webinars')
const PYTHON_ORCHESTRATOR = join(PROJECT_ROOT, 'scripts', 'webinar', 'master_orchestrator.py')

/**
 * Get webinar by ID from files
 */
async function getWebinarById(webinarId: string): Promise<any | null> {
  try {
    const filePath = join(WEBINARS_DIR, `${webinarId}.json`)
    
    if (!existsSync(filePath)) {
      return null
    }

    const content = await readFile(filePath, 'utf-8')
    const webinar = JSON.parse(content)
    
    return {
      ...webinar,
      id: webinar.webinar_id || webinarId,
      source: 'file'
    }
  } catch (error) {
    console.error(`Error reading webinar ${webinarId}:`, error)
    return null
  }
}

/**
 * GET /api/webinar/[id]
 * 
 * Gets detailed information about a specific webinar.
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const webinarId = params.id

    // VALIDATION: Check webinar ID format
    if (!webinarId || typeof webinarId !== 'string') {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid webinar ID'
        },
        { status: 400 }
      )
    }

    // Get webinar
    const webinar = await getWebinarById(webinarId)

    if (!webinar) {
      return NextResponse.json(
        {
          success: false,
          error: `Webinar ${webinarId} not found`
        },
        { status: 404 }
      )
    }

    return NextResponse.json(
      {
        success: true,
        webinar,
        timestamp: new Date().toISOString()
      },
      {
        headers: {
          'Cache-Control': 'public, max-age=300' // Cache for 5 minutes
        }
      }
    )
  } catch (error: any) {
    console.error('Error getting webinar:', error)
    
    return NextResponse.json(
      {
        success: false,
        error: error.message || 'Failed to get webinar'
      },
      { status: 500 }
    )
  }
}

