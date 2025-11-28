import { NextRequest, NextResponse } from 'next/server'
export const dynamic = 'force-dynamic'
import { exec } from 'child_process'
import { promisify } from 'util'
import { join } from 'path'
import { withPublicApi } from '@/lib/middleware/api-wrapper'
import { readFile, readdir } from 'fs/promises'
import { existsSync } from 'fs'

const execAsync = promisify(exec)

/**
 * Webinar List API Route
 * 
 * Pattern: API × WEBINAR × LIST × INTEGRATION × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Lists all available webinars from database or JSON files.
 */

const PROJECT_ROOT = process.cwd()
const WEBINARS_DIR = join(PROJECT_ROOT, 'webinars')
const PYTHON_ORCHESTRATOR = join(PROJECT_ROOT, 'scripts', 'webinar', 'master_orchestrator.py')

/**
 * Get webinars from JSON files (fallback)
 */
async function getWebinarsFromFiles(): Promise<any[]> {
  try {
    if (!existsSync(WEBINARS_DIR)) {
      return []
    }

    const files = await readdir(WEBINARS_DIR)
    const jsonFiles = files.filter(f => f.endsWith('.json'))
    
    const webinars = []
    for (const file of jsonFiles) {
      try {
        const content = await readFile(join(WEBINARS_DIR, file), 'utf-8')
        const webinar = JSON.parse(content)
        webinars.push({
          ...webinar,
          id: webinar.webinar_id || file.replace('.json', ''),
          source: 'file'
        })
      } catch (e) {
        // Skip invalid JSON files
        continue
      }
    }

    return webinars.sort((a, b) => {
      const dateA = new Date(a.scheduled_time || a.created_at || 0).getTime()
      const dateB = new Date(b.scheduled_time || b.created_at || 0).getTime()
      return dateB - dateA // Most recent first
    })
  } catch (error) {
    console.error('Error reading webinar files:', error)
    return []
  }
}

/**
 * GET /api/webinar/list
 * 
 * Lists all available webinars.
 * 
 * Query params:
 *   - limit: number (optional, default: 50)
 *   - upcoming: boolean (optional, filter upcoming only)
 */
export const GET = withPublicApi(async (request: NextRequest) => {
  try {
    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get('limit') || '50', 10)
    const upcomingOnly = searchParams.get('upcoming') === 'true'

    // Get webinars from files (database access via Python would be better, but this works)
    const webinars = await getWebinarsFromFiles()

    // Filter upcoming if requested
    let filtered = webinars
    if (upcomingOnly) {
      const now = new Date()
      filtered = webinars.filter(w => {
        const scheduled = new Date(w.scheduled_time || w.created_at || 0)
        return scheduled > now
      })
    }

    // Apply limit
    const limited = filtered.slice(0, limit)

    return NextResponse.json(
      {
        success: true,
        webinars: limited,
        total: filtered.length,
        limit,
        upcomingOnly,
        timestamp: new Date().toISOString()
      },
      {
        headers: {
          'Cache-Control': 'public, max-age=60' // Cache for 1 minute
        }
      }
    )
  } catch (error: any) {
    console.error('Error listing webinars:', error)
    
    return NextResponse.json(
      {
        success: false,
        error: error.message || 'Failed to list webinars',
        webinars: []
      },
      { status: 500 }
    )
  }
})

