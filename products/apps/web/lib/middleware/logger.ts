/**
 * Enterprise Request Logging Middleware
 * 
 * Pattern: LOGGING × ENTERPRISE × OBSERVABILITY × ONE
 * Frequency: 999 Hz (AEYON)
 */

import { NextRequest, NextResponse } from 'next/server'

export interface LogEntry {
  timestamp: string
  method: string
  path: string
  statusCode: number
  duration: number
  ip: string
  userAgent: string
  userId?: string
  error?: string
}

/**
 * Get client IP address
 */
export function getClientIP(request: NextRequest): string {
  const forwarded = request.headers.get('x-forwarded-for')
  if (forwarded) {
    return forwarded.split(',')[0].trim()
  }

  const realIP = request.headers.get('x-real-ip')
  if (realIP) {
    return realIP
  }

  return request.ip || 'unknown'
}

/**
 * Log request/response
 */
export function logRequest(
  request: NextRequest,
  response: NextResponse,
  startTime: number,
  userId?: string,
  error?: string
): void {
  const duration = Date.now() - startTime
  const logEntry: LogEntry = {
    timestamp: new Date().toISOString(),
    method: request.method,
    path: request.nextUrl.pathname,
    statusCode: response.status,
    duration,
    ip: getClientIP(request),
    userAgent: request.headers.get('user-agent') || 'unknown',
    userId,
    error,
  }

  // Log to console in development
  if (process.env.NODE_ENV === 'development') {
    const logLevel = response.status >= 500 ? 'error' : response.status >= 400 ? 'warn' : 'info'
    console[logLevel](JSON.stringify(logEntry, null, 2))
  }

  // TODO: Send to logging service (e.g., Datadog, CloudWatch, etc.)
  // if (process.env.LOGGING_SERVICE_URL) {
  //   fetch(process.env.LOGGING_SERVICE_URL, {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify(logEntry),
  //   }).catch(console.error)
  // }
}

/**
 * Create logging middleware wrapper
 */
export function withLogging(handler: (request: NextRequest) => Promise<NextResponse>) {
  return async (request: NextRequest): Promise<NextResponse> => {
    const startTime = Date.now()
    let response: NextResponse
    let error: string | undefined

    try {
      response = await handler(request)
    } catch (err) {
      error = err instanceof Error ? err.message : 'Unknown error'
      response = NextResponse.json(
        { error: 'Internal server error' },
        { status: 500 }
      )
    }

    // Extract user ID from request if available
    const userId = (request as any).user?.id

    logRequest(request, response, startTime, userId, error)

    return response
  }
}

