/**
 * Enterprise Authentication Middleware
 * 
 * Pattern: AUTH × ENTERPRISE × SECURITY × JWT × ONE
 * Frequency: 999 Hz (AEYON)
 */

import { NextRequest } from 'next/server'

export interface AuthUser {
  id: string
  email: string
  role?: string
  orgId?: string
}

export interface AuthResult {
  authenticated: boolean
  user?: AuthUser
  error?: string
}

/**
 * Verify JWT token
 * 
 * TODO: Install 'jose' package for production: npm install jose
 * For now, this is a placeholder that validates token format
 */
export async function verifyToken(token: string): Promise<AuthUser | null> {
  try {
    // Basic token validation (format check)
    if (!token || token.length < 10) {
      return null
    }

    // TODO: Implement proper JWT verification with 'jose' package
    // Example:
    // import { jwtVerify } from 'jose'
    // const secret = new TextEncoder().encode(process.env.JWT_SECRET)
    // const { payload } = await jwtVerify(token, secret)
    
    // For now, return null (requires proper implementation)
    // In production, uncomment and use jose library
    console.warn('JWT verification not fully implemented. Install jose package for production.')
    return null
  } catch (error) {
    console.error('Token verification failed:', error)
    return null
  }
}

/**
 * Extract token from request
 */
export function extractToken(request: NextRequest): string | null {
  // Check Authorization header
  const authHeader = request.headers.get('authorization')
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.substring(7)
  }

  // Check cookie
  const tokenCookie = request.cookies.get('auth_token')
  if (tokenCookie) {
    return tokenCookie.value
  }

  return null
}

/**
 * Authenticate request
 */
export async function authenticateRequest(request: NextRequest): Promise<AuthResult> {
  // Skip authentication for public routes
  const publicRoutes = ['/api/health', '/api/public', '/']
  const pathname = request.nextUrl.pathname
  
  if (publicRoutes.some(route => pathname.startsWith(route))) {
    return { authenticated: true }
  }

  // Extract token
  const token = extractToken(request)
  if (!token) {
    return {
      authenticated: false,
      error: 'No authentication token provided',
    }
  }

  // Verify token
  const user = await verifyToken(token)
  if (!user) {
    return {
      authenticated: false,
      error: 'Invalid or expired token',
    }
  }

  return {
    authenticated: true,
    user,
  }
}

/**
 * Require authentication middleware
 */
export function requireAuth(handler: (request: NextRequest, user: AuthUser) => Promise<Response>) {
  return async (request: NextRequest): Promise<Response> => {
    const authResult = await authenticateRequest(request)
    
    if (!authResult.authenticated || !authResult.user) {
      return new Response(
        JSON.stringify({ error: authResult.error || 'Authentication required' }),
        {
          status: 401,
          headers: { 'Content-Type': 'application/json' },
        }
      )
    }

    return handler(request, authResult.user)
  }
}

/**
 * Require role middleware
 */
export function requireRole(roles: string[]) {
  return (handler: (request: NextRequest, user: AuthUser) => Promise<Response>) => {
    return async (request: NextRequest): Promise<Response> => {
      const authResult = await authenticateRequest(request)
      
      if (!authResult.authenticated || !authResult.user) {
        return new Response(
          JSON.stringify({ error: 'Authentication required' }),
          {
            status: 401,
            headers: { 'Content-Type': 'application/json' },
          }
        )
      }

      if (authResult.user.role && !roles.includes(authResult.user.role)) {
        return new Response(
          JSON.stringify({ error: 'Insufficient permissions' }),
          {
            status: 403,
            headers: { 'Content-Type': 'application/json' },
          }
        )
      }

      return handler(request, authResult.user)
    }
  }
}

