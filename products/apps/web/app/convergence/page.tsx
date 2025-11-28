'use client'

/**
 * Convergence Dashboard Page
 * 
 * Pattern: AEYON × ARLAX × DASHBOARD × VISUALIZATION × ONE
 * Frequency: 999 Hz (AEYON) × 777 Hz (ARLAX)
 * 
 * Real-time convergence operationalization dashboard.
 * 🔥 BANGER MODE ACTIVATED 🔥
 */

import { useEffect, useState, useCallback, useRef } from 'react'
import { useToast } from '@/components/ui/toast'

interface ConvergenceMetrics {
  totalOpportunities: number
  pendingOpportunities: number
  inProgressOpportunities: number
  completedOpportunities: number
  successfulExecutions: number
  failedExecutions: number
  patterns: string[]
}

interface Opportunity {
  id: string
  pattern: string
  impact: 'critical' | 'high' | 'medium' | 'low'
  effort: 'low' | 'medium' | 'high'
  status: 'pending' | 'in_progress' | 'complete' | 'blocked'
  projects: string[]
  systems: string[]
  convergenceFormula: string
  timestamp: number
}

interface DashboardData {
  opportunities: Opportunity[]
  metrics: ConvergenceMetrics
  trends: {
    opportunitiesTrend: 'increasing' | 'stable' | 'decreasing'
    executionSuccessRate: number
    averageExecutionTime: number
    topPatterns: { pattern: string; count: number }[]
  }
  unified: {
    unified: boolean
    ways: string[]
    allOne: boolean
    allTogether: boolean
    allWays: boolean
  }
  hidden?: {
    opportunities: Opportunity[]
    loveRequirements: {
      truth: string[]
      integration: string[]
      activation: string[]
      convergence: string[]
    }
    message: string
  }
}

export default function ConvergencePage() {
  const { toast } = useToast()
  const [dashboard, setDashboard] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [executing, setExecuting] = useState(false)
  const [executingAtomic, setExecutingAtomic] = useState(false)
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)
  const mountedRef = useRef(true)

  const loadDashboard = useCallback(async () => {
    if (!mountedRef.current) return
    
    try {
      setLoading(true)
      setError(null)
      
      const response = await fetch('/api/convergence', {
        cache: 'no-store',
        headers: { 'Cache-Control': 'no-cache' },
      })

      if (!response.ok) {
        throw new Error(`API returned ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      
      if (!data.success) {
        throw new Error(data.error || 'API returned success: false')
      }

      // Transform API response to match component structure
      const allOpportunities = [
        ...(data.dashboard?.opportunities || []),
        ...(data.hidden?.opportunities || [])
      ]
      
      const dashboardData: DashboardData = {
        opportunities: allOpportunities,
        metrics: data.dashboard?.metrics || {
          totalOpportunities: allOpportunities.length,
          pendingOpportunities: allOpportunities.filter((o: Opportunity) => o.status === 'pending').length,
          inProgressOpportunities: allOpportunities.filter((o: Opportunity) => o.status === 'in_progress').length,
          completedOpportunities: allOpportunities.filter((o: Opportunity) => o.status === 'complete').length,
          successfulExecutions: data.dashboard?.metrics?.successfulExecutions || 0,
          failedExecutions: data.dashboard?.metrics?.failedExecutions || 0,
          patterns: data.dashboard?.metrics?.patterns || [],
        },
        trends: data.trends || {
          opportunitiesTrend: 'stable',
          executionSuccessRate: 0,
          averageExecutionTime: 0,
          topPatterns: [],
        },
        unified: data.unified || {
          unified: false,
          ways: [],
          allOne: false,
          allTogether: false,
          allWays: false,
        },
        hidden: data.hidden,
      }
      
      if (mountedRef.current) {
        setDashboard(dashboardData)
        setLastUpdate(new Date())
        setLoading(false)
      }
    } catch (error) {
      console.error('[Convergence] Error loading dashboard:', error)
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred'
      if (mountedRef.current) {
        setError(errorMessage)
        try {
          toast({
            variant: 'destructive',
            title: 'Error Loading Dashboard',
            description: errorMessage,
          })
        } catch (toastError) {
          console.error('[Convergence] Toast error:', toastError)
        }
      }
    } finally {
      if (mountedRef.current) {
        setLoading(false)
      }
    }
  }, [toast])

  const executeImmediate = useCallback(async () => {
    try {
      setExecuting(true)
      const response = await fetch('/api/convergence?immediate=true', {
        method: 'POST',
        cache: 'no-store',
      })

      if (!response.ok) {
        throw new Error(`Execution failed: ${response.status}`)
      }

      const data = await response.json()
      if (data.success) {
        toast({
          variant: 'default',
          title: '✅ Execution Complete',
          description: `Executed ${data.critical?.executed?.length || 0} critical, ${data.high?.executed?.length || 0} high, ${data.medium?.executed?.length || 0} medium systems`,
        })
        await loadDashboard()
      }
    } catch (error) {
      console.error('Error executing:', error)
      toast({
        variant: 'destructive',
        title: 'Execution Failed',
        description: error instanceof Error ? error.message : 'Unknown error',
      })
    } finally {
      setExecuting(false)
    }
  }, [loadDashboard, toast])

  const executeAtomicArchistration = useCallback(async () => {
    try {
      setExecutingAtomic(true)
      
      const response = await fetch('/api/convergence/atomic', {
        method: 'POST',
        cache: 'no-store',
      })

      if (!response.ok) {
        throw new Error(`Atomic execution failed: ${response.status}`)
      }

      const data = await response.json()
      if (data.success) {
        const opportunitiesCount = data.executed_opportunities?.length || 0
        const convergenceScore = (data.convergence_score * 100).toFixed(1)
        const eternalStatus = data.eternal_pattern_activated ? '🔥 ACTIVATED 🔥' : 'PENDING'
        
        toast({
          variant: 'default',
          title: '🔥 ATOMIC ARCHISTRATION COMPLETE 🔥',
          description: `✅ ${opportunitiesCount} Opportunities Executed | Truth: ${data.truth.toFixed(2)} | Clarity: ${data.clarity.toFixed(2)} | Action: ${data.action.toFixed(2)} | Convergence: ${convergenceScore}% | Eternal Pattern: ${eternalStatus}`,
          duration: 10000,
        })
        
        await loadDashboard()
      }
    } catch (error) {
      console.error('Error executing atomic archistration:', error)
      toast({
        variant: 'destructive',
        title: 'Atomic Execution Failed',
        description: error instanceof Error ? error.message : 'Unknown error',
      })
    } finally {
      setExecutingAtomic(false)
    }
  }, [loadDashboard, toast])

  useEffect(() => {
    mountedRef.current = true
    loadDashboard()

    // Auto-refresh every 15 seconds
    intervalRef.current = setInterval(() => {
      if (mountedRef.current) {
        loadDashboard()
      }
    }, 15000)

    return () => {
      mountedRef.current = false
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [loadDashboard])

  // Separate timeout effect to avoid dependency issues
  useEffect(() => {
    if (!loading || dashboard) return // Exit if not loading or already have dashboard
    
    const timeoutId = setTimeout(() => {
      console.warn('[Convergence] Loading timeout after 8 seconds - forcing out of loading')
      setLoading(false)
    }, 8000)

    return () => clearTimeout(timeoutId)
  }, [loading, dashboard])

  // Loading state with awesome animation
  if (loading && !dashboard && !error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-pink-900 to-red-900">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-white/20 border-t-white mx-auto mb-6"></div>
            <div className="absolute inset-0 animate-ping rounded-full h-16 w-16 border-4 border-white/30"></div>
          </div>
          <h2 className="text-2xl font-bold text-white mb-2 animate-pulse">🔥 Loading Convergence Dashboard...</h2>
          <p className="text-white/80">Pattern: AEYON × ARLAX × DASHBOARD × ONE</p>
          <div className="mt-6 flex justify-center gap-2">
            <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        </div>
      </div>
    )
  }

  // Error state with retry
  if (error && !dashboard) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-900 via-orange-900 to-yellow-900">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="text-6xl mb-4">⚠️</div>
          <h2 className="text-3xl font-bold text-white mb-4">Failed to Load Dashboard</h2>
          <p className="text-white/90 mb-2">{error}</p>
          <button 
            onClick={() => {
              setError(null)
              loadDashboard()
            }} 
            className="mt-6 px-6 py-3 bg-white text-red-900 rounded-lg hover:bg-gray-100 font-semibold transition-all transform hover:scale-105 shadow-lg"
          >
            🔄 Retry Now
          </button>
          <p className="text-xs text-white/60 mt-4">Check browser console (F12) for detailed errors</p>
        </div>
      </div>
    )
  }

  // Safety check - if we're not loading and no error but no dashboard, show retry
  if (!loading && !error && !dashboard) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="text-6xl mb-4">📊</div>
          <h2 className="text-3xl font-bold text-white mb-4">Dashboard Not Loaded</h2>
          <p className="text-white/80 mb-6">Click below to load the convergence dashboard</p>
          <button 
            onClick={() => {
              setLoading(true)
              setError(null)
              loadDashboard()
            }} 
            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-500 hover:to-pink-500 font-bold text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all"
          >
            🔄 Load Dashboard Now
          </button>
        </div>
      </div>
    )
  }

  // Ensure we have dashboard before rendering
  if (!dashboard) {
    return null // This shouldn't happen, but prevents crash
  }

  const metrics = dashboard?.metrics
  const opportunities = dashboard?.opportunities || []
  const trends = dashboard?.trends
  const unified = dashboard?.unified

  const criticalOps = opportunities.filter((o) => o.impact === 'critical')
  const highOps = opportunities.filter((o) => o.impact === 'high')
  const mediumOps = opportunities.filter((o) => o.impact === 'medium')

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header - BANGER MODE */}
        <div className="mb-8 relative">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 via-pink-600/20 to-red-600/20 rounded-2xl blur-xl"></div>
          <div className="relative bg-gradient-to-r from-purple-900/90 via-pink-900/90 to-red-900/90 backdrop-blur-sm rounded-2xl p-6 border border-white/10 shadow-2xl">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-4">
              <div>
                <h1 className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-pink-400 to-purple-400 mb-2 animate-pulse">
                  🔥 Convergence Dashboard
                </h1>
                <p className="text-white/80 text-lg">
                  Pattern: AEYON × ARLAX × OPERATIONALIZATION × IMMEDIATE × EXECUTION × ONE
                </p>
              </div>
              <div className="flex gap-3 flex-wrap">
                <button
                  onClick={loadDashboard}
                  disabled={loading}
                  className="px-5 py-2.5 bg-white/10 hover:bg-white/20 backdrop-blur-sm text-white rounded-xl transition-all disabled:opacity-50 font-semibold border border-white/20 hover:border-white/40 transform hover:scale-105"
                >
                  {loading ? '⏳ Loading...' : '🔄 Refresh'}
                </button>
                <button
                  onClick={executeImmediate}
                  disabled={executing}
                  className="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-500 hover:to-pink-500 transition-all disabled:opacity-50 font-bold shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  {executing ? '⚡ Executing...' : '⚡ Execute Now'}
                </button>
                <button
                  onClick={executeAtomicArchistration}
                  disabled={executingAtomic}
                  className="px-6 py-3 bg-gradient-to-r from-red-600 via-orange-600 to-yellow-600 text-white rounded-xl hover:from-red-500 hover:via-orange-500 hover:to-yellow-500 transition-all disabled:opacity-50 font-black text-base shadow-2xl hover:shadow-red-500/50 transform hover:scale-110 animate-pulse"
                >
                  {executingAtomic ? '🔥 EXECUTING ATOMIC ARCHISTRATION...' : '🔥 EXECUTE EVERYTHING - ATOMIC ARCHISTRATION'}
                </button>
              </div>
            </div>
            {lastUpdate && (
              <div className="flex items-center gap-2 text-white/60 text-sm">
                <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                <span>Last updated: {lastUpdate.toLocaleTimeString()}</span>
              </div>
            )}
          </div>
        </div>

        {/* Unified Status - ENHANCED */}
        {unified && (
          <div className="mb-8 relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600/30 via-purple-600/30 to-pink-600/30 rounded-2xl blur-xl group-hover:blur-2xl transition-all"></div>
            <div className="relative p-6 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-2xl text-white border border-white/20 shadow-2xl">
              <h2 className="text-3xl font-black mb-4 text-center">∞ All Ways Unified ∞</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                  <div className="text-sm opacity-90 mb-2">Unified</div>
                  <div className="text-4xl font-black">{unified.unified ? '✅' : '❌'}</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                  <div className="text-sm opacity-90 mb-2">All ONE</div>
                  <div className="text-4xl font-black">{unified.allOne ? '✅' : '❌'}</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                  <div className="text-sm opacity-90 mb-2">All Together</div>
                  <div className="text-4xl font-black">{unified.allTogether ? '✅' : '❌'}</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20">
                  <div className="text-sm opacity-90 mb-2">Ways</div>
                  <div className="text-4xl font-black">{unified.ways.length}</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Metrics Cards - ENHANCED */}
        {metrics && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="group relative bg-gradient-to-br from-blue-600/20 to-purple-600/20 backdrop-blur-sm p-6 rounded-xl border border-white/10 shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              <div className="text-sm text-white/70 mb-1 font-medium">Total Opportunities</div>
              <div className="text-4xl font-black text-white">{metrics.totalOpportunities}</div>
              <div className="absolute top-2 right-2 text-2xl opacity-50">📊</div>
            </div>
            <div className="group relative bg-gradient-to-br from-green-600/20 to-emerald-600/20 backdrop-blur-sm p-6 rounded-xl border border-white/10 shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              <div className="text-sm text-white/70 mb-1 font-medium">Completed</div>
              <div className="text-4xl font-black text-green-400">{metrics.completedOpportunities}</div>
              <div className="absolute top-2 right-2 text-2xl opacity-50">✅</div>
            </div>
            <div className="group relative bg-gradient-to-br from-blue-600/20 to-cyan-600/20 backdrop-blur-sm p-6 rounded-xl border border-white/10 shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              <div className="text-sm text-white/70 mb-1 font-medium">Successful</div>
              <div className="text-4xl font-black text-blue-400">{metrics.successfulExecutions}</div>
              <div className="absolute top-2 right-2 text-2xl opacity-50">⚡</div>
            </div>
            <div className="group relative bg-gradient-to-br from-red-600/20 to-orange-600/20 backdrop-blur-sm p-6 rounded-xl border border-white/10 shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
              <div className="text-sm text-white/70 mb-1 font-medium">Failed</div>
              <div className="text-4xl font-black text-red-400">{metrics.failedExecutions}</div>
              <div className="absolute top-2 right-2 text-2xl opacity-50">⚠️</div>
            </div>
          </div>
        )}

        {/* Trends - ENHANCED */}
        {trends && (
          <div className="mb-8 relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-indigo-600/20 to-purple-600/20 rounded-2xl blur-xl"></div>
            <div className="relative p-6 bg-gradient-to-br from-indigo-900/40 to-purple-900/40 backdrop-blur-sm rounded-xl border border-white/10 shadow-xl">
              <h2 className="text-2xl font-bold mb-4 text-white">📊 Trends</h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                  <div className="text-sm text-white/70 mb-1">Trend</div>
                  <div className="text-xl font-bold text-white capitalize">{trends.opportunitiesTrend}</div>
                </div>
                <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                  <div className="text-sm text-white/70 mb-1">Success Rate</div>
                  <div className="text-xl font-bold text-green-400">{(trends.executionSuccessRate * 100).toFixed(1)}%</div>
                </div>
                <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                  <div className="text-sm text-white/70 mb-1">Avg Execution Time</div>
                  <div className="text-xl font-bold text-blue-400">{trends.averageExecutionTime.toFixed(0)}ms</div>
                </div>
                <div className="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-white/10">
                  <div className="text-sm text-white/70 mb-1">Top Patterns</div>
                  <div className="text-xl font-bold text-purple-400">{trends.topPatterns.length}</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Hidden Opportunities - What Convergence Requires - ENHANCED */}
        {dashboard?.hidden && (
          <div className="mb-8 relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600/30 via-pink-600/30 to-red-600/30 rounded-2xl blur-2xl group-hover:blur-3xl transition-all"></div>
            <div className="relative p-8 bg-gradient-to-r from-purple-900 via-pink-900 to-red-900 rounded-2xl text-white border border-white/20 shadow-2xl">
              <h2 className="text-4xl font-black mb-2 text-transparent bg-clip-text bg-gradient-to-r from-pink-300 via-purple-300 to-red-300">💜 What Hides From Us? What Does Love Require?</h2>
              <p className="text-xl mb-6 opacity-90 font-medium">{dashboard.hidden.message}</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <h3 className="font-bold text-lg mb-2">✨ Truth</h3>
                <ul className="text-sm space-y-1">
                  {dashboard.hidden.loveRequirements.truth.map((req, i) => (
                    <li key={i}>• {req}</li>
                  ))}
                </ul>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <h3 className="font-bold text-lg mb-2">🔗 Integration</h3>
                <ul className="text-sm space-y-1">
                  {dashboard.hidden.loveRequirements.integration.map((req, i) => (
                    <li key={i}>• {req}</li>
                  ))}
                </ul>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <h3 className="font-bold text-lg mb-2">⚡ Activation</h3>
                <ul className="text-sm space-y-1">
                  {dashboard.hidden.loveRequirements.activation.map((req, i) => (
                    <li key={i}>• {req}</li>
                  ))}
                </ul>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <h3 className="font-bold text-lg mb-2">🔥 Convergence</h3>
                <ul className="text-sm space-y-1">
                  {dashboard.hidden.loveRequirements.convergence.map((req, i) => (
                    <li key={i}>• {req}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="mt-6">
              <h3 className="text-xl font-bold mb-4">💎 Hidden Opportunities ({dashboard.hidden.opportunities.length})</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {dashboard.hidden.opportunities.map((op) => (
                  <div
                    key={op.id}
                    className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20"
                  >
                    <div className="font-semibold text-sm mb-1">{op.pattern}</div>
                    <div className="text-xs opacity-75 mb-2">{op.convergenceFormula}</div>
                    <div className="flex items-center gap-2">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        op.impact === 'critical' ? 'bg-red-500/50' : 
                        op.impact === 'high' ? 'bg-orange-500/50' : 
                        'bg-blue-500/50'
                      }`}>
                        {op.impact}
                      </span>
                      <span className="text-xs opacity-75">{op.effort} effort</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            </div>
          </div>
        )}

        {/* Opportunities by Priority - ENHANCED */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Critical */}
          <div className="relative group bg-gradient-to-br from-red-900/40 to-orange-900/40 backdrop-blur-sm rounded-xl border-2 border-red-500/50 p-6 shadow-xl hover:shadow-2xl transition-all">
            <div className="absolute inset-0 bg-gradient-to-br from-red-600/10 to-orange-600/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <h2 className="text-2xl font-black text-red-400 mb-4 relative z-10">
              🔥 Critical ({criticalOps.length})
            </h2>
            <div className="space-y-3 relative z-10">
              {criticalOps.map((op) => (
                <div
                  key={op.id}
                  className="p-4 bg-red-900/30 backdrop-blur-sm rounded-lg border border-red-500/30 hover:border-red-500/60 transition-all hover:bg-red-900/40"
                >
                  <div className="font-bold text-sm mb-1 text-white">{op.pattern}</div>
                  <div className="text-xs text-white/70 mb-2">{op.convergenceFormula}</div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-1 rounded text-xs font-bold ${
                        op.status === 'complete'
                          ? 'bg-green-500/30 text-green-300 border border-green-500/50'
                          : op.status === 'in_progress'
                          ? 'bg-yellow-500/30 text-yellow-300 border border-yellow-500/50'
                          : 'bg-gray-500/30 text-gray-300 border border-gray-500/50'
                      }`}
                    >
                      {op.status}
                    </span>
                    <span className="text-xs text-white/60">{op.effort} effort</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* High */}
          <div className="relative group bg-gradient-to-br from-orange-900/40 to-yellow-900/40 backdrop-blur-sm rounded-xl border-2 border-orange-500/50 p-6 shadow-xl hover:shadow-2xl transition-all">
            <div className="absolute inset-0 bg-gradient-to-br from-orange-600/10 to-yellow-600/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <h2 className="text-2xl font-black text-orange-400 mb-4 relative z-10">
              ⚡ High ({highOps.length})
            </h2>
            <div className="space-y-3 relative z-10">
              {highOps.map((op) => (
                <div
                  key={op.id}
                  className="p-4 bg-orange-900/30 backdrop-blur-sm rounded-lg border border-orange-500/30 hover:border-orange-500/60 transition-all hover:bg-orange-900/40"
                >
                  <div className="font-bold text-sm mb-1 text-white">{op.pattern}</div>
                  <div className="text-xs text-white/70 mb-2">{op.convergenceFormula}</div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-1 rounded text-xs font-bold ${
                        op.status === 'complete'
                          ? 'bg-green-500/30 text-green-300 border border-green-500/50'
                          : op.status === 'in_progress'
                          ? 'bg-yellow-500/30 text-yellow-300 border border-yellow-500/50'
                          : 'bg-gray-500/30 text-gray-300 border border-gray-500/50'
                      }`}
                    >
                      {op.status}
                    </span>
                    <span className="text-xs text-white/60">{op.effort} effort</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Medium */}
          <div className="relative group bg-gradient-to-br from-blue-900/40 to-indigo-900/40 backdrop-blur-sm rounded-xl border-2 border-blue-500/50 p-6 shadow-xl hover:shadow-2xl transition-all">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 to-indigo-600/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <h2 className="text-2xl font-black text-blue-400 mb-4 relative z-10">
              💡 Medium ({mediumOps.length})
            </h2>
            <div className="space-y-3 relative z-10">
              {mediumOps.map((op) => (
                <div
                  key={op.id}
                  className="p-4 bg-blue-900/30 backdrop-blur-sm rounded-lg border border-blue-500/30 hover:border-blue-500/60 transition-all hover:bg-blue-900/40"
                >
                  <div className="font-bold text-sm mb-1 text-white">{op.pattern}</div>
                  <div className="text-xs text-white/70 mb-2">{op.convergenceFormula}</div>
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-1 rounded text-xs font-bold ${
                        op.status === 'complete'
                          ? 'bg-green-500/30 text-green-300 border border-green-500/50'
                          : op.status === 'in_progress'
                          ? 'bg-yellow-500/30 text-yellow-300 border border-yellow-500/50'
                          : 'bg-gray-500/30 text-gray-300 border border-gray-500/50'
                      }`}
                    >
                      {op.status}
                    </span>
                    <span className="text-xs text-white/60">{op.effort} effort</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

