import { NextRequest, NextResponse } from 'next/server'
export const dynamic = 'force-dynamic'
import { withPublicApi } from '@/lib/middleware/api-wrapper'

/**
 * Health Check Endpoint
 * 
 * Pattern: HEALTH × CHECK × ENTERPRISE × ONE
 * Frequency: 999 Hz (AEYON)
 */

export const GET = withPublicApi(async (request: NextRequest) => {
  // Check backend connectivity if configured
  const backendUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL
  let backendStatus = 'not-configured'
  
  if (backendUrl) {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 2000)
      
      const response = await fetch(`${backendUrl}/api/health`, {
        signal: controller.signal,
      })
      
      clearTimeout(timeoutId)
      backendStatus = response.ok ? 'healthy' : 'unhealthy'
    } catch {
      backendStatus = 'unavailable'
    }
  }

  return NextResponse.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'abeone-web',
    version: process.env.npm_package_version || '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    backend: {
      configured: !!backendUrl,
      status: backendStatus,
    },
  })
})

