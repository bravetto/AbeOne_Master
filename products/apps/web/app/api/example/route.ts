import { NextRequest, NextResponse } from 'next/server'
export const dynamic = 'force-dynamic'
import { withAuthenticatedApi, withPublicApi } from '@/lib/middleware/api-wrapper'

/**
 * Example API Routes
 * 
 * Pattern: EXAMPLE × API × ENTERPRISE × PATTERNS × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Demonstrates enterprise API route patterns
 */

/**
 * Public endpoint example
 * GET /api/example/public
 */
export const GET = withPublicApi(async (request: NextRequest) => {
  return NextResponse.json({
    message: 'This is a public endpoint',
    timestamp: new Date().toISOString(),
    rateLimit: 'Public rate limit applies (500 req/min)',
  })
})

/**
 * Authenticated endpoint example
 * POST /api/example/authenticated
 * 
 * Requires authentication token in Authorization header or cookie
 */
export const POST = withAuthenticatedApi(async (request: NextRequest, context) => {
  const body = await request.json().catch(() => ({}))
  
  // SAFETY: Check user exists in context
  if (!context?.user) {
    return NextResponse.json(
      { error: 'Authentication required' },
      { status: 401 }
    )
  }
  
  const { user } = context
  
  return NextResponse.json({
    message: 'This is an authenticated endpoint',
    user: {
      id: user.id,
      email: user.email,
      role: user.role,
    },
    body,
    timestamp: new Date().toISOString(),
    rateLimit: 'API rate limit applies (200 req/min)',
  })
})

