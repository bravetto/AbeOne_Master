/**
 * Enterprise API Route Wrapper
 * 
 * Pattern: WRAPPER × ENTERPRISE × MIDDLEWARE × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Unified wrapper combining:
 * - Rate limiting
 * - Authentication
 * - Request logging
 * - Error handling
 * - Security headers
 */

import { NextRequest, NextResponse } from 'next/server'
import { RateLimitResult, endpointRateLimiters, defaultRateLimiter } from './rate-limiter'
import { authenticateRequest, AuthResult, AuthUser, requireAuth, requireRole } from './auth'
import { withLogging, getClientIP } from './logger'

export interface RouteConfig {
  /**
   * Rate limiting configuration
   * - 'default': Use default rate limiter (100 req/min)
   * - 'api': Use API rate limiter (200 req/min)
   * - 'auth': Use auth rate limiter (10 req/min)
   * - 'public': Use public rate limiter (500 req/min)
   * - 'none': Skip rate limiting
   */
  rateLimit?: 'default' | 'api' | 'auth' | 'public' | 'none'
  
  /**
   * Authentication requirements
   * - 'none': No authentication required
   * - 'required': Authentication required
   * - string[]: Required roles (e.g., ['admin', 'user'])
   */
  auth?: 'none' | 'required' | string[]
  
  /**
   * Enable request logging
   */
  logging?: boolean
  
  /**
   * Custom error handler
   */
  onError?: (error: Error, request: NextRequest) => NextResponse
}

export type RouteHandler = (
  request: NextRequest,
  context?: {
    user?: AuthUser
    rateLimit?: RateLimitResult
  }
) => Promise<NextResponse>

/**
 * Get rate limiter based on config
 */
function getRateLimiter(config: RouteConfig) {
  if (config.rateLimit === 'none') return null
  
  switch (config.rateLimit) {
    case 'api':
      return endpointRateLimiters.api
    case 'auth':
      return endpointRateLimiters.auth
    case 'public':
      return endpointRateLimiters.public
    case 'default':
    default:
      return defaultRateLimiter
  }
}

/**
 * Add security headers to response
 */
function addSecurityHeaders(response: NextResponse): NextResponse {
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-XSS-Protection', '1; mode=block')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  
  if (process.env.NODE_ENV === 'production') {
    response.headers.set(
      'Strict-Transport-Security',
      'max-age=31536000; includeSubDomains; preload'
    )
  }
  
  return response
}

/**
 * Create rate limit error response
 */
function createRateLimitResponse(rateLimit: RateLimitResult): NextResponse {
  const response = NextResponse.json(
    {
      error: 'Too many requests',
      message: 'Rate limit exceeded. Please try again later.',
      retryAfter: Math.ceil((rateLimit.resetTime - Date.now()) / 1000),
    },
    { status: 429 }
  )
  
  response.headers.set('Retry-After', String(Math.ceil((rateLimit.resetTime - Date.now()) / 1000)))
  response.headers.set('X-RateLimit-Limit', String(rateLimit.limit))
  response.headers.set('X-RateLimit-Remaining', String(rateLimit.remaining))
  response.headers.set('X-RateLimit-Reset', String(Math.ceil(rateLimit.resetTime / 1000)))
  
  return addSecurityHeaders(response)
}

/**
 * Create authentication error response
 */
function createAuthErrorResponse(error: string, status: number = 401): NextResponse {
  return addSecurityHeaders(
    NextResponse.json(
      { error: error },
      { status }
    )
  )
}

/**
 * Enterprise API route wrapper
 * 
 * Usage:
 * ```ts
 * export const GET = withApiWrapper(
 *   async (request, { user, rateLimit }) => {
 *     return NextResponse.json({ data: 'success' })
 *   },
 *   {
 *     rateLimit: 'api',
 *     auth: 'required',
 *     logging: true,
 *   }
 * )
 * ```
 */
export function withApiWrapper(
  handler: RouteHandler,
  config: RouteConfig = {}
): (request: NextRequest) => Promise<NextResponse> {
  // Default config
  const finalConfig: RouteConfig = {
    rateLimit: config.rateLimit ?? 'default',
    auth: config.auth ?? 'none',
    logging: config.logging ?? true,
    ...config,
  }

  // Wrap handler with logging if enabled
  const wrappedHandler = finalConfig.logging
    ? withLogging(async (request: NextRequest) => {
        return await executeHandler(request, handler, finalConfig)
      })
    : async (request: NextRequest) => {
        return await executeHandler(request, handler, finalConfig)
      }

  return wrappedHandler
}

/**
 * Execute handler with middleware
 */
async function executeHandler(
  request: NextRequest,
  handler: RouteHandler,
  config: RouteConfig
): Promise<NextResponse> {
  try {
    // 1. Rate limiting
    const rateLimiter = getRateLimiter(config)
    let rateLimitResult: RateLimitResult | undefined

    if (rateLimiter) {
      const clientIP = getClientIP(request)
      const endpoint = request.nextUrl.pathname.split('/').pop() || 'default'
      const rateLimitKey = `${clientIP}:${endpoint}`
      
      rateLimitResult = rateLimiter.check(rateLimitKey)

      if (!rateLimitResult.allowed) {
        return createRateLimitResponse(rateLimitResult)
      }
    }

    // 2. Authentication
    let authUser: AuthUser | undefined

    if (config.auth === 'required' || Array.isArray(config.auth)) {
      const authResult: AuthResult = await authenticateRequest(request)

      if (!authResult.authenticated || !authResult.user) {
        return createAuthErrorResponse(
          authResult.error || 'Authentication required',
          401
        )
      }

      // Check roles if specified
      if (Array.isArray(config.auth) && config.auth.length > 0) {
        if (!authResult.user.role || !config.auth.includes(authResult.user.role)) {
          return createAuthErrorResponse('Insufficient permissions', 403)
        }
      }

      authUser = authResult.user
    }

    // 3. Execute handler
    const response = await handler(request, {
      user: authUser,
      rateLimit: rateLimitResult,
    })

    // 4. Add rate limit headers to successful responses
    if (rateLimitResult) {
      response.headers.set('X-RateLimit-Limit', String(rateLimitResult.limit))
      response.headers.set('X-RateLimit-Remaining', String(rateLimitResult.remaining))
      response.headers.set('X-RateLimit-Reset', String(Math.ceil(rateLimitResult.resetTime / 1000)))
    }

    // 5. Add security headers
    return addSecurityHeaders(response)
  } catch (error) {
    // Handle errors
    if (config.onError) {
      return config.onError(
        error instanceof Error ? error : new Error('Unknown error'),
        request
      )
    }

    // Default error handling
    const errorMessage = error instanceof Error ? error.message : 'Internal server error'
    console.error('API route error:', error)

    return addSecurityHeaders(
      NextResponse.json(
        { error: 'Internal server error', message: errorMessage },
        { status: 500 }
      )
    )
  }
}

/**
 * Convenience wrappers for common patterns
 */

/**
 * Public API route (no auth, default rate limit)
 */
export function withPublicApi(handler: RouteHandler) {
  return withApiWrapper(handler, {
    rateLimit: 'public',
    auth: 'none',
    logging: true,
  })
}

/**
 * Authenticated API route (auth required, API rate limit)
 */
export function withAuthenticatedApi(handler: RouteHandler) {
  return withApiWrapper(handler, {
    rateLimit: 'api',
    auth: 'required',
    logging: true,
  })
}

/**
 * Admin API route (admin role required, strict rate limit)
 */
export function withAdminApi(handler: RouteHandler) {
  return withApiWrapper(handler, {
    rateLimit: 'auth',
    auth: ['admin'],
    logging: true,
  })
}

