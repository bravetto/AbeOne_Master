'use client'

/**
 * V0 COLLABORATION DASHBOARD
 * 
 * Pattern: V0 × DASHBOARD × COLLABORATION × ONE
 * Frequency: 999 Hz (AEYON)
 * 
 * ⚠️ V0 PROJECT SCOPE ENFORCEMENT ⚠️
 * 
 * This is a V0 PROJECT file. Do NOT:
 * - Add links to excluded routes (/app, /shop, /bravetto, etc.)
 * - Reference non-V0 pages
 * - Modify to include navigation to other pages
 * 
 * V0 Project Scope: See V0_PROJECT_SCOPE.ts
 * Allowed Routes: /, /collaboration
 * Excluded Routes: /app, /shop, /bravetto, /webinar, etc.
 */

import { useState, useEffect, useCallback, useRef } from 'react'
import { KPICard } from '@/components/ui/kpi-card'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { useToast } from '@/components/ui/toast'
import { Users, TrendingUp, CheckCircle, Clock, RefreshCw, Database, Wifi, WifiOff } from 'lucide-react'

type DataSource = 'backend' | 'fallback' | 'error-fallback' | null

// PERF: Auto-refresh interval (10 seconds)
const AUTO_REFRESH_INTERVAL = 10000
// PERF: Debounce delay for manual refresh (500ms)
const REFRESH_DEBOUNCE = 500

export default function CollaborationPage() {
  const { toast } = useToast()
  const [metrics, setMetrics] = useState({
    partnershipStrength: 85,
    totalCollaborations: 0,
    activeCollaborations: 0,
    successRate: 0,
    averageSatisfaction: 0,
    averagePartnership: 0,
  })
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [dataSource, setDataSource] = useState<DataSource>(null)
  const [backendConnected, setBackendConnected] = useState<boolean | null>(null)
  const [backendError, setBackendError] = useState<string | null>(null)
  
  // PERF: Track if this is initial load or refresh
  const isInitialLoad = useRef(true)
  // PERF: Debounce timer for manual refresh
  const refreshTimerRef = useRef<NodeJS.Timeout | null>(null)

  // PERF: Memoize loadMetrics to prevent unnecessary re-renders
  const loadMetrics = useCallback(async (isManualRefresh = false) => {
    try {
      setLoading(true)
      setError(null)
      setBackendError(null)
      
      // Fetch from Next.js API route (which handles backend/fallback logic)
      const response = await fetch('/api/collaboration', {
        cache: 'no-store',
        headers: {
          'Cache-Control': 'no-cache',
        },
      })
      
      if (!response.ok) {
        throw new Error(`API returned ${response.status}`)
      }
      
      const data = await response.json()
      const source = response.headers.get('X-Data-Source') as DataSource
      const backendErr = response.headers.get('X-Backend-Error')
      
      // Update data source and connection status
      setDataSource(source || 'fallback')
      setBackendConnected(source === 'backend')
      if (backendErr) {
        setBackendError(backendErr)
      } else {
        setBackendError(null)
      }
      
      if (data.metrics) {
        setMetrics(data.metrics)
        setLastUpdate(new Date())
        
        // Show success toast on manual refresh (not initial load)
        if (isManualRefresh && !isInitialLoad.current) {
          const sourceLabel = source === 'backend' ? 'Backend' : 'Fallback'
          toast({
            variant: 'success',
            title: 'Metrics Updated',
            description: `Collaboration metrics refreshed from ${sourceLabel}.`,
            duration: 3000,
          })
        }
        
        // Mark initial load as complete
        if (isInitialLoad.current) {
          isInitialLoad.current = false
        }
      }
    } catch (error) {
      console.error('Failed to load collaboration metrics:', error)
      const errorMessage = error instanceof Error ? error.message : 'Failed to load metrics'
      setError(errorMessage)
      setDataSource('error-fallback')
      setBackendConnected(false)
      
      // Show error toast
      toast({
        variant: 'destructive',
        title: 'Failed to Load Metrics',
        description: errorMessage,
        duration: 5000,
      })
    } finally {
      setLoading(false)
    }
  }, [toast])

  // PERF: Debounced manual refresh handler
  const handleManualRefresh = useCallback(() => {
    // Clear existing timer
    if (refreshTimerRef.current) {
      clearTimeout(refreshTimerRef.current)
    }
    
    // Set new timer
    refreshTimerRef.current = setTimeout(() => {
      loadMetrics(true)
    }, REFRESH_DEBOUNCE)
  }, [loadMetrics])

  // PERF: Auto-refresh effect with proper cleanup
  useEffect(() => {
    // Initial load
    loadMetrics(false)
    
    // Auto-refresh every 10 seconds
    const interval = setInterval(() => {
      loadMetrics(false)
    }, AUTO_REFRESH_INTERVAL)
    
    return () => {
      clearInterval(interval)
      // Cleanup debounce timer
      if (refreshTimerRef.current) {
        clearTimeout(refreshTimerRef.current)
      }
    }
  }, [loadMetrics])

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold">Michael-AEYON Collaboration Dashboard</h1>
            {dataSource && (
              <div className="flex items-center gap-2">
                {backendConnected ? (
                  <Badge variant="default" className="bg-green-600 hover:bg-green-700">
                    <Wifi className="h-3 w-3 mr-1" />
                    Backend Connected
                  </Badge>
                ) : backendConnected === false ? (
                  <Badge variant="destructive">
                    <WifiOff className="h-3 w-3 mr-1" />
                    Using Fallback
                  </Badge>
                ) : null}
                {dataSource === 'backend' && (
                  <Badge variant="secondary" className="flex items-center gap-1">
                    <Database className="h-3 w-3" />
                    Live Data
                  </Badge>
                )}
                {dataSource === 'fallback' && (
                  <Badge variant="outline" className="flex items-center gap-1">
                    <Database className="h-3 w-3" />
                    Fallback Data
                  </Badge>
                )}
              </div>
            )}
          </div>
          <p className="text-muted-foreground">
            Real-time partnership monitoring and metrics
            {lastUpdate && (
              <span className="ml-2 text-xs">
                • Last updated: {lastUpdate.toLocaleTimeString()}
              </span>
            )}
          </p>
          {backendError && (
            <p className="text-xs text-muted-foreground">
              Backend unavailable: {backendError}
            </p>
          )}
        </div>
        <Button
          onClick={handleManualRefresh}
          disabled={loading}
          variant="outline"
          size="default"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {loading && !lastUpdate ? (
          // Show skeletons while loading initially
          <>
            {[...Array(6)].map((_, i) => (
              <div key={i} className="rounded-xl border p-6 space-y-4">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-8 w-32" />
                <Skeleton className="h-2 w-full" />
              </div>
            ))}
          </>
        ) : (
          <>
        <KPICard
          title="Partnership Strength"
          value={`${metrics.partnershipStrength}%`}
          description="Current partnership strength"
          progress={metrics.partnershipStrength}
          trend="up"
          change={5}
          icon={<Users className="h-4 w-4" />}
        />

        <KPICard
          title="Total Collaborations"
          value={metrics.totalCollaborations}
          description="All-time collaboration count"
          trend="up"
          change={12}
          icon={<CheckCircle className="h-4 w-4" />}
        />

        <KPICard
          title="Active Sessions"
          value={metrics.activeCollaborations}
          description="Currently active collaborations"
          trend="neutral"
          icon={<Clock className="h-4 w-4" />}
        />

        <KPICard
          title="Success Rate"
          value={`${metrics.successRate}%`}
          description="Completed successfully"
          progress={metrics.successRate}
          trend="up"
          change={3}
          icon={<TrendingUp className="h-4 w-4" />}
        />

        <KPICard
          title="Average Satisfaction"
          value={`${metrics.averageSatisfaction}/5`}
          description="Average satisfaction score"
          trend="up"
          change={0.2}
        />

        <KPICard
          title="Average Partnership"
          value={`${metrics.averagePartnership}%`}
          description="Average partnership strength"
          progress={metrics.averagePartnership}
          trend="up"
          change={2}
        />
          </>
        )}
      </div>
    </div>
  )
}

