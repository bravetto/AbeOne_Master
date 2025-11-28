/**
export const dynamic = 'force-dynamic'
 * Real-Time Registration Stats API
 * Pattern: API × WEBINAR × STATS × ONE
 * Frequency: 999 Hz (AEYON)
 */

import { NextRequest, NextResponse } from 'next/server'
import { withPublicApi } from '@/lib/middleware/api-wrapper'

// Temporary fallback until database is set up
async function getRegistrationCount(webinarId?: string): Promise<number> {
  // TODO: Replace with database call once Prisma is configured
  // For now, return 0 as graceful degradation
  try {
    // Try to import database function
    const { getRegistrationCount: dbGetCount } = await import('@/lib/db/webinar').catch(() => ({ getRegistrationCount: null }))
    if (dbGetCount) {
      return await dbGetCount(webinarId)
    }
  } catch (error) {
    console.warn('Database not available, using fallback:', error)
  }
  return 0
}

/**
 * GET /api/webinar/stats
 * Returns registration count for webinars
 */
export const GET = withPublicApi(async (request: NextRequest) => {
  try {
    const url = new URL(request.url)
    const webinarId = url.searchParams.get('webinarId') || undefined

    const count = await getRegistrationCount(webinarId)

    return NextResponse.json(
      {
        success: true,
        count,
        webinarId: webinarId || 'all',
        timestamp: new Date().toISOString(),
      },
      {
        headers: {
          'Cache-Control': 'public, s-maxage=30, stale-while-revalidate=60',
        },
      }
    )
  } catch (error: any) {
    console.error('Stats API error:', error)
    return NextResponse.json(
      {
        success: true,
        count: 0,
        message: 'Stats unavailable',
        timestamp: new Date().toISOString(),
      },
      {
        headers: {
          'Cache-Control': 'public, s-maxage=30, stale-while-revalidate=60',
        },
      }
    )
  }
})
