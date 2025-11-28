import { NextRequest, NextResponse } from 'next/server'
export const dynamic = 'force-dynamic'
import { withPublicApi } from '@/lib/middleware/api-wrapper'
import { env } from '@/lib/env'
import {
  CollaborationMetricsResponse,
  validateCollaborationMetricsResponse,
  normalizeCollaborationMetricsResponse,
} from '@/lib/types/collaboration'

/**
 * Collaboration Metrics API Route
 * 
 * Pattern: API × COLLABORATION × METRICS × ENTERPRISE × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Fetches collaboration metrics from FastAPI backend with fallback.
 * Enterprise-grade: rate-limited, logged, error-handled, validated.
 */

// OPTIMIZE: Use centralized env config
const BACKEND_API_URL = env.backendApiUrl || 'http://localhost:8000'
const BACKEND_TIMEOUT = 5000 // 5 seconds

/**
 * Fetch metrics from FastAPI backend
 * 
 * VALIDATION: Validates response schema before returning
 */
async function fetchBackendMetrics(): Promise<CollaborationMetricsResponse> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), BACKEND_TIMEOUT)

  try {
    const response = await fetch(`${BACKEND_API_URL}/api/collaboration/metrics`, {
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`)
    }

    const data = await response.json()
    
    // VALIDATION: Validate and normalize response
    if (!validateCollaborationMetricsResponse(data)) {
      console.warn('Backend response validation failed, normalizing:', data)
      return normalizeCollaborationMetricsResponse(data)
    }

    return data as CollaborationMetricsResponse
  } catch (error: any) {
    clearTimeout(timeoutId)
    
    if (error.name === 'AbortError') {
      throw new Error('Backend request timeout')
    }
    
    throw error
  }
}

/**
 * Get fallback metrics (used when backend is unavailable)
 * 
 * SIMPLIFY: Returns properly typed fallback data matching backend schema
 */
function getFallbackMetrics(): CollaborationMetricsResponse {
  return {
    metrics: {
      partnershipStrength: 85,
      totalCollaborations: 0,
      activeCollaborations: 0,
      successRate: 0,
      averageSatisfaction: 0,
      averagePartnership: 85,
    },
    activeSessions: [], // SCHEMA FIX: Ensure activeSessions array matches backend
    timestamp: new Date().toISOString(),
    source: 'fallback',
  }
}

/**
 * GET /api/collaboration
 * 
 * Returns collaboration metrics from backend or fallback data.
 */
export const GET = withPublicApi(async (request: NextRequest) => {
  try {
    // Try backend first
    try {
      const backendData = await fetchBackendMetrics()
      
      // VALIDATION: Ensure data is properly typed
      const response: CollaborationMetricsResponse = {
        ...backendData,
        source: 'backend',
        timestamp: new Date().toISOString(),
      }
      
      return NextResponse.json(response, {
        headers: {
          'Cache-Control': 'no-store, must-revalidate',
          'X-Data-Source': 'backend',
        },
      })
    } catch (backendError) {
      // Backend unavailable, use fallback
      console.warn('Backend unavailable, using fallback data:', backendError)
      
      const fallbackData = getFallbackMetrics()
      const errorMessage = backendError instanceof Error ? backendError.message : 'Unknown error'
      
      return NextResponse.json(
        {
          ...fallbackData,
          error: errorMessage,
        },
        {
          headers: {
            'Cache-Control': 'no-store, must-revalidate',
            'X-Data-Source': 'fallback',
            'X-Backend-Error': errorMessage,
          },
        }
      )
    }
  } catch (error: any) {
    // Unexpected error
    console.error('Error fetching collaboration metrics:', error)
    
    const fallbackData = getFallbackMetrics()
    
    return NextResponse.json(
      {
        ...fallbackData,
        source: 'error-fallback',
        error: error.message || 'Failed to fetch collaboration metrics',
      },
      {
        status: 500,
        headers: {
          'Cache-Control': 'no-store, must-revalidate',
          'X-Data-Source': 'error-fallback',
        },
      }
    )
  }
})

