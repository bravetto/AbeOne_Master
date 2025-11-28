import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Enterprise Middleware Stack
 * 
 * Pattern: MIDDLEWARE × ENTERPRISE × SECURITY × PERFORMANCE × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Middleware Order:
 * 1. Security Headers
 * 2. Rate Limiting
 * 3. Authentication/Authorization
 * 4. Request Logging
 * 5. CORS Handling
 * 6. Request Validation
 */

// Rate limiting store (in-memory for now, can be upgraded to Redis)
const rateLimitStore = new Map<string, { count: number; resetTime: number }>()

// Rate limit configuration
const RATE_LIMIT_CONFIG = {
  windowMs: 60 * 1000, // 1 minute
  maxRequests: 100, // 100 requests per minute
  burstLimit: 20, // 20 requests burst
}

/**
 * Check rate limit for IP address
 */
function checkRateLimit(ip: string): { allowed: boolean; remaining: number; resetTime: number } {
  const now = Date.now()
  const key = `rate_limit:${ip}`
  const record = rateLimitStore.get(key)

  if (!record || now > record.resetTime) {
    // New window or expired
    rateLimitStore.set(key, {
      count: 1,
      resetTime: now + RATE_LIMIT_CONFIG.windowMs,
    })
    return {
      allowed: true,
      remaining: RATE_LIMIT_CONFIG.maxRequests - 1,
      resetTime: now + RATE_LIMIT_CONFIG.windowMs,
    }
  }

  if (record.count >= RATE_LIMIT_CONFIG.maxRequests) {
    return {
      allowed: false,
      remaining: 0,
      resetTime: record.resetTime,
    }
  }

  // Increment count
  record.count++
  rateLimitStore.set(key, record)

  return {
    allowed: true,
    remaining: RATE_LIMIT_CONFIG.maxRequests - record.count,
    resetTime: record.resetTime,
  }
}

/**
 * Clean up expired rate limit records
 */
function cleanupRateLimitStore() {
  const now = Date.now()
  // SAFETY: Convert Map entries to array for iteration (TypeScript compatibility)
  const entries = Array.from(rateLimitStore.entries())
  for (const [key, record] of entries) {
    if (now > record.resetTime) {
      rateLimitStore.delete(key)
    }
  }
}

// Cleanup every 5 minutes
if (typeof setInterval !== 'undefined') {
  setInterval(cleanupRateLimitStore, 5 * 60 * 1000)
}

/**
 * Get client IP address
 */
function getClientIP(request: NextRequest): string {
  // Check various headers for IP (for proxies/load balancers)
  const forwarded = request.headers.get('x-forwarded-for')
  if (forwarded) {
    return forwarded.split(',')[0].trim()
  }

  const realIP = request.headers.get('x-real-ip')
  if (realIP) {
    return realIP
  }

  // Fallback to connection IP
  return request.ip || 'unknown'
}

/**
 * Add security headers to response
 */
function addSecurityHeaders(response: NextResponse): NextResponse {
  // Security headers
  response.headers.set('X-Content-Type-Options', 'nosniff')
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-XSS-Protection', '1; mode=block')
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin')
  response.headers.set(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=()'
  )

  // HSTS (only in production)
  if (process.env.NODE_ENV === 'production') {
    response.headers.set(
      'Strict-Transport-Security',
      'max-age=31536000; includeSubDomains; preload'
    )
  }

  return response
}

/**
 * Main middleware function
 */
export function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // Skip middleware for static assets and API routes (handled separately)
  if (
    pathname.startsWith('/_next') ||
    pathname.startsWith('/static') ||
    pathname.startsWith('/favicon.ico') ||
    pathname.startsWith('/api/health')
  ) {
    return NextResponse.next()
  }

  // Get client IP
  const clientIP = getClientIP(request)

  // Rate limiting (skip for health checks)
  if (!pathname.startsWith('/api/health')) {
    const rateLimit = checkRateLimit(clientIP)
    
    if (!rateLimit.allowed) {
      const response = NextResponse.json(
        {
          error: 'Too many requests',
          message: 'Rate limit exceeded. Please try again later.',
          retryAfter: Math.ceil((rateLimit.resetTime - Date.now()) / 1000),
        },
        { status: 429 }
      )
      
      response.headers.set('Retry-After', String(Math.ceil((rateLimit.resetTime - Date.now()) / 1000)))
      response.headers.set('X-RateLimit-Limit', String(RATE_LIMIT_CONFIG.maxRequests))
      response.headers.set('X-RateLimit-Remaining', String(rateLimit.remaining))
      response.headers.set('X-RateLimit-Reset', String(Math.ceil(rateLimit.resetTime / 1000)))
      
      return addSecurityHeaders(response)
    }

    // Add rate limit headers to successful responses
    const response = NextResponse.next()
    response.headers.set('X-RateLimit-Limit', String(RATE_LIMIT_CONFIG.maxRequests))
    response.headers.set('X-RateLimit-Remaining', String(rateLimit.remaining))
    response.headers.set('X-RateLimit-Reset', String(Math.ceil(rateLimit.resetTime / 1000)))
    
    // SAFETY: AbëViSiONs Blank Page Prevention
    response.headers.set('X-AbeViSiONs-Page', pathname)
    response.headers.set('X-AbeViSiONs-Timestamp', String(Date.now()))
    
    return addSecurityHeaders(response)
  }

  // Create response with security headers
  const response = NextResponse.next()
  
  // SAFETY: AbëViSiONs Blank Page Prevention
  response.headers.set('X-AbeViSiONs-Page', pathname)
  response.headers.set('X-AbeViSiONs-Timestamp', String(Date.now()))
  
  return addSecurityHeaders(response)
}

/**
 * Middleware configuration
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}

