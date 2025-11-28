/**
 * Backend Health Check Hook
 * 
 * Pattern: HEALTH × CHECK × CONNECTION × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * Monitors backend connection status and provides health information
 */

import { useState, useEffect, useCallback } from 'react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const HEALTH_CHECK_INTERVAL = 30000 // 30 seconds

export interface BackendHealth {
  status: 'healthy' | 'unhealthy' | 'checking' | 'unavailable' | 'not-configured'
  lastCheck: Date | null
  error?: string
  operational?: boolean
}

export function useBackendHealth() {
  const [health, setHealth] = useState<BackendHealth>({
    status: 'checking',
    lastCheck: null,
  })

  const checkHealth = useCallback(async () => {
    if (!API_URL) {
      setHealth({
        status: 'not-configured',
        lastCheck: new Date(),
        error: 'Backend API URL not configured',
      })
      return
    }

    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 2000) // 2 second timeout

      const response = await fetch(`${API_URL}/health`, {
        signal: controller.signal,
        cache: 'no-store',
      })

      clearTimeout(timeoutId)

      if (response.ok) {
        const data = await response.json()
        setHealth({
          status: 'healthy',
          lastCheck: new Date(),
          operational: data.operational ?? true,
        })
      } else {
        setHealth({
          status: 'unhealthy',
          lastCheck: new Date(),
          error: `Backend returned ${response.status}`,
        })
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        setHealth({
          status: 'unavailable',
          lastCheck: new Date(),
          error: 'Backend connection timeout',
        })
      } else {
        setHealth({
          status: 'unavailable',
          lastCheck: new Date(),
          error: error.message || 'Backend server not running or not accessible',
        })
      }
    }
  }, [])

  useEffect(() => {
    // Initial check
    checkHealth()

    // Set up periodic health checks
    const intervalId = setInterval(checkHealth, HEALTH_CHECK_INTERVAL)

    return () => {
      clearInterval(intervalId)
    }
  }, [checkHealth])

  return {
    health,
    checkHealth,
    isHealthy: health.status === 'healthy',
    isChecking: health.status === 'checking',
  }
}

